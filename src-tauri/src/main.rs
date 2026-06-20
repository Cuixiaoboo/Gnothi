// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use log::info;
use rusqlite::{Connection, params};
use serde::{Deserialize, Serialize};
use std::fs;
use std::sync::Mutex;
use tauri::State;

// 数据库连接状态
struct DbState {
    conn: Mutex<Connection>,
}

// 笔记模型
#[derive(Debug, Serialize, Deserialize)]
struct Note {
    id: i32,
    title: String,
    content: String,
    created_at: String,
    updated_at: String,
    sort_order: i32,
}

// 待办模型
#[derive(Debug, Serialize, Deserialize)]
struct Todo {
    id: i32,
    title: String,
    status: String,
    priority: String,
    due_date: String,
    notes: String,
    completed_at: String,
    created_at: String,
    updated_at: String,
}

// 日报列定义
#[derive(Debug, Serialize, Deserialize, Clone)]
struct Column {
    key: String,
    label: String,
}

// 日报模型
#[derive(Debug, Serialize, Deserialize)]
struct DailyReport {
    date: String,
    columns: Vec<Column>,
    rows: Vec<serde_json::Value>,
    exists: bool,
    updated_at: String,
}

fn now_str() -> String {
    chrono::Utc::now().format("%Y-%m-%d %H:%M:%S").to_string()
}

// ========== 笔记命令 ==========

#[tauri::command]
fn get_notes(state: State<DbState>) -> Result<Vec<Note>, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    let mut stmt = conn
        .prepare("SELECT id, title, content, created_at, updated_at, sort_order FROM notes ORDER BY sort_order ASC, updated_at DESC")
        .map_err(|e| e.to_string())?;

    let notes = stmt
        .query_map([], |row| {
            Ok(Note {
                id: row.get(0)?,
                title: row.get(1)?,
                content: row.get(2)?,
                created_at: row.get(3)?,
                updated_at: row.get(4)?,
                sort_order: row.get(5)?,
            })
        })
        .map_err(|e| e.to_string())?
        .collect::<Result<Vec<_>, _>>()
        .map_err(|e| e.to_string())?;

    Ok(notes)
}

#[tauri::command]
fn get_note(state: State<DbState>, id: i32) -> Result<Note, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    conn.query_row(
        "SELECT id, title, content, created_at, updated_at, sort_order FROM notes WHERE id = ?1",
        [id],
        |row| {
            Ok(Note {
                id: row.get(0)?,
                title: row.get(1)?,
                content: row.get(2)?,
                created_at: row.get(3)?,
                updated_at: row.get(4)?,
                sort_order: row.get(5)?,
            })
        },
    )
    .map_err(|e| e.to_string())
}

#[tauri::command]
fn create_note(state: State<DbState>, title: String, content: Option<String>) -> Result<Note, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    let now = now_str();
    let note_content = content.unwrap_or_default();

    let min_order: i32 = conn
        .query_row("SELECT COALESCE(MIN(sort_order), 0) FROM notes", [], |row| row.get(0))
        .map_err(|e| e.to_string())?;

    let new_order = min_order - 1;

    conn.execute(
        "INSERT INTO notes (title, content, created_at, updated_at, sort_order) VALUES (?1, ?2, ?3, ?4, ?5)",
        params![title, note_content, now, now, new_order],
    )
    .map_err(|e| e.to_string())?;

    let id = conn.last_insert_rowid() as i32;
    info!("创建笔记: [{}] {}", id, title);

    Ok(Note {
        id,
        title,
        content: note_content,
        created_at: now.clone(),
        updated_at: now,
        sort_order: new_order,
    })
}

#[tauri::command]
fn update_note(state: State<DbState>, id: i32, title: Option<String>, content: Option<String>) -> Result<Note, String> {
    let now = now_str();

    {
        let conn = state.conn.lock().map_err(|e| e.to_string())?;
        let mut sql = String::from("UPDATE notes SET updated_at = ?1");
        let mut param_idx = 2u32;

        if title.is_some() {
            sql += &format!(", title = ?{}", param_idx);
            param_idx += 1;
        }
        if content.is_some() {
            sql += &format!(", content = ?{}", param_idx);
            param_idx += 1;
        }
        sql += &format!(" WHERE id = ?{}", param_idx);

        // Build params dynamically
        let mut all_params: Vec<Box<dyn rusqlite::types::ToSql>> = vec![Box::new(now.clone())];
        if let Some(ref t) = title {
            all_params.push(Box::new(t.clone()));
        }
        if let Some(ref c) = content {
            all_params.push(Box::new(c.clone()));
        }
        all_params.push(Box::new(id));

        conn.execute(&sql, rusqlite::params_from_iter(all_params.iter().map(|p| p.as_ref())))
            .map_err(|e| e.to_string())?;
    } // conn dropped here

    get_note(state, id)
}

#[tauri::command]
fn delete_note(state: State<DbState>, id: i32) -> Result<bool, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    conn.execute("DELETE FROM notes WHERE id = ?1", [id])
        .map_err(|e| e.to_string())?;
    info!("删除笔记: [{}]", id);
    Ok(true)
}

#[tauri::command]
fn reorder_notes(state: State<DbState>, ids: Vec<i32>) -> Result<bool, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    for (index, note_id) in ids.iter().enumerate() {
        conn.execute(
            "UPDATE notes SET sort_order = ?1 WHERE id = ?2",
            params![index as i32, note_id],
        )
        .map_err(|e| e.to_string())?;
    }
    Ok(true)
}

// ========== 待办命令 ==========

#[tauri::command]
fn get_todos(state: State<DbState>, status: Option<String>) -> Result<Vec<Todo>, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;

    let sql = match &status {
        Some(s) if s != "all" => {
            "SELECT id, title, status, priority, due_date, notes, completed_at, created_at, updated_at FROM todos WHERE status = ?1 ORDER BY created_at DESC"
        }
        _ => "SELECT id, title, status, priority, due_date, notes, completed_at, created_at, updated_at FROM todos ORDER BY created_at DESC",
    };

    let mut stmt = conn.prepare(sql).map_err(|e| e.to_string())?;

    let mapper = |row: &rusqlite::Row| -> rusqlite::Result<Todo> {
        Ok(Todo {
            id: row.get(0)?,
            title: row.get(1)?,
            status: row.get(2)?,
            priority: row.get(3)?,
            due_date: row.get(4)?,
            notes: row.get(5)?,
            completed_at: row.get(6)?,
            created_at: row.get(7)?,
            updated_at: row.get(8)?,
        })
    };

    let todos = match &status {
        Some(s) if s != "all" => stmt.query_map(params![s], mapper),
        _ => stmt.query_map([], mapper),
    }
    .map_err(|e| e.to_string())?
    .collect::<Result<Vec<_>, _>>()
    .map_err(|e| e.to_string())?;

    Ok(todos)
}

#[tauri::command]
fn create_todo(
    state: State<DbState>,
    title: String,
    status: Option<String>,
    priority: Option<String>,
    due_date: Option<String>,
    notes: Option<String>,
) -> Result<Todo, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    let now = now_str();

    conn.execute(
        "INSERT INTO todos (title, status, priority, due_date, notes, created_at, updated_at) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
        params![
            title,
            status.as_deref().unwrap_or("pending"),
            priority.as_deref().unwrap_or("medium"),
            due_date.as_deref().unwrap_or(""),
            notes.as_deref().unwrap_or(""),
            now,
            now
        ],
    )
    .map_err(|e| e.to_string())?;

    let id = conn.last_insert_rowid() as i32;
    info!("创建待办: [{}] {}", id, title);

    Ok(Todo {
        id,
        title,
        status: status.unwrap_or_else(|| "pending".to_string()),
        priority: priority.unwrap_or_else(|| "medium".to_string()),
        due_date: due_date.unwrap_or_default(),
        notes: notes.unwrap_or_default(),
        completed_at: String::new(),
        created_at: now.clone(),
        updated_at: now,
    })
}

#[tauri::command]
fn update_todo(
    state: State<DbState>,
    id: i32,
    title: Option<String>,
    status: Option<String>,
    priority: Option<String>,
    due_date: Option<String>,
    notes: Option<String>,
) -> Result<Todo, String> {
    let now = now_str();

    {
        let conn = state.conn.lock().map_err(|e| e.to_string())?;
        let mut sql = String::from("UPDATE todos SET updated_at = ?1");
        let mut params_vec: Vec<Box<dyn rusqlite::types::ToSql>> = vec![Box::new(now.clone())];
        let mut idx = 2u32;

        macro_rules! add_field {
            ($field:expr, $col:expr) => {
                if $field.is_some() {
                    sql += &format!(", {} = ?{}", $col, idx);
                    params_vec.push(Box::new($field.clone().unwrap()));
                    idx += 1;
                }
            };
        }

        add_field!(title, "title");
        add_field!(priority, "priority");
        add_field!(due_date, "due_date");
        add_field!(notes, "notes");

        if let Some(ref s) = status {
            sql += &format!(", status = ?{}", idx);
            params_vec.push(Box::new(s.clone()));
            idx += 1;
            if s == "completed" {
                sql += &format!(", completed_at = ?{}", idx);
                params_vec.push(Box::new(now.clone()));
                idx += 1;
            }
        }

        sql += &format!(" WHERE id = ?{}", idx);
        params_vec.push(Box::new(id));

        conn.execute(&sql, rusqlite::params_from_iter(params_vec.iter().map(|p| p.as_ref())))
            .map_err(|e| e.to_string())?;
    } // conn dropped

    // Re-read the updated todo
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    conn.query_row(
        "SELECT id, title, status, priority, due_date, notes, completed_at, created_at, updated_at FROM todos WHERE id = ?1",
        [id],
        |row| {
            Ok(Todo {
                id: row.get(0)?,
                title: row.get(1)?,
                status: row.get(2)?,
                priority: row.get(3)?,
                due_date: row.get(4)?,
                notes: row.get(5)?,
                completed_at: row.get(6)?,
                created_at: row.get(7)?,
                updated_at: row.get(8)?,
            })
        },
    )
    .map_err(|e| e.to_string())
}

#[tauri::command]
fn delete_todo(state: State<DbState>, id: i32) -> Result<bool, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    conn.execute("DELETE FROM todos WHERE id = ?1", [id])
        .map_err(|e| e.to_string())?;
    info!("删除待办: [{}]", id);
    Ok(true)
}

// ========== 日报命令 ==========

#[tauri::command]
fn get_report_dates(state: State<DbState>) -> Result<Vec<String>, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    let mut stmt = conn
        .prepare("SELECT date FROM daily_reports")
        .map_err(|e| e.to_string())?;

    let dates = stmt
        .query_map([], |row| row.get(0))
        .map_err(|e| e.to_string())?
        .collect::<Result<Vec<String>, _>>()
        .map_err(|e| e.to_string())?;

    Ok(dates)
}

#[tauri::command]
fn get_report(state: State<DbState>, date: String) -> Result<DailyReport, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    let result = conn.query_row(
        "SELECT columns, rows, updated_at FROM daily_reports WHERE date = ?1",
        [&date],
        |row| {
            let columns_str: String = row.get(0)?;
            let rows_str: String = row.get(1)?;
            let updated_at: String = row.get(2)?;
            let columns: Vec<Column> = serde_json::from_str(&columns_str).unwrap_or_default();
            let rows: Vec<serde_json::Value> = serde_json::from_str(&rows_str).unwrap_or_default();
            Ok((columns, rows, updated_at))
        },
    );

    match result {
        Ok((columns, rows, updated_at)) => Ok(DailyReport {
            date,
            columns,
            rows,
            exists: true,
            updated_at,
        }),
        Err(_) => Ok(DailyReport {
            date,
            columns: Vec::new(),
            rows: Vec::new(),
            exists: false,
            updated_at: String::new(),
        }),
    }
}

#[tauri::command]
fn save_report(state: State<DbState>, date: String, columns: Vec<Column>, rows: Vec<serde_json::Value>) -> Result<bool, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    let now = now_str();
    let columns_json = serde_json::to_string(&columns).map_err(|e| e.to_string())?;
    let rows_json = serde_json::to_string(&rows).map_err(|e| e.to_string())?;

    conn.execute(
        "INSERT OR REPLACE INTO daily_reports (date, columns, rows, created_at, updated_at) VALUES (?1, ?2, ?3, COALESCE((SELECT created_at FROM daily_reports WHERE date = ?1), ?4), ?4)",
        params![date, columns_json, rows_json, now],
    )
    .map_err(|e| e.to_string())?;

    info!("保存日报: {}", date);
    Ok(true)
}

#[tauri::command]
fn delete_report(state: State<DbState>, date: String) -> Result<bool, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    conn.execute("DELETE FROM daily_reports WHERE date = ?1", [&date])
        .map_err(|e| e.to_string())?;
    info!("删除日报: {}", date);
    Ok(true)
}

// ========== 名言命令 ==========

#[tauri::command]
fn get_mottos(state: State<DbState>) -> Result<Vec<serde_json::Value>, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    let mut stmt = conn
        .prepare("SELECT id, content, created_at FROM mottos ORDER BY id ASC")
        .map_err(|e| e.to_string())?;

    let mottos = stmt
        .query_map([], |row| {
            Ok(serde_json::json!({
                "id": row.get::<_, i32>(0)?,
                "content": row.get::<_, String>(1)?,
                "created_at": row.get::<_, String>(2).unwrap_or_default()
            }))
        })
        .map_err(|e| e.to_string())?
        .collect::<Result<Vec<_>, _>>()
        .map_err(|e| e.to_string())?;

    Ok(mottos)
}

#[tauri::command]
fn create_motto(state: State<DbState>, content: String) -> Result<serde_json::Value, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    let now = now_str();

    conn.execute(
        "INSERT INTO mottos (content, created_at) VALUES (?1, ?2)",
        params![content, now],
    )
    .map_err(|e| e.to_string())?;

    let id = conn.last_insert_rowid() as i32;
    info!("创建名言: [{}] {}", id, content);

    Ok(serde_json::json!({
        "id": id,
        "content": content,
        "created_at": now
    }))
}

#[tauri::command]
fn update_motto(state: State<DbState>, id: i32, content: String) -> Result<bool, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;

    conn.execute(
        "UPDATE mottos SET content = ?1 WHERE id = ?2",
        params![content, id],
    )
    .map_err(|e| e.to_string())?;

    info!("更新名言: [{}] {}", id, content);
    Ok(true)
}

#[tauri::command]
fn delete_motto(state: State<DbState>, id: i32) -> Result<bool, String> {
    let conn = state.conn.lock().map_err(|e| e.to_string())?;
    conn.execute("DELETE FROM mottos WHERE id = ?1", [id])
        .map_err(|e| e.to_string())?;
    info!("删除名言: [{}]", id);
    Ok(true)
}

// ========== 主函数 ==========

fn main() {
    // 创建日志和数据目录
    fs::create_dir_all("log").expect("Failed to create log directory");
    fs::create_dir_all("data").expect("Failed to create data directory");

    // 检查日志文件大小，超过 10MB 则清空
    let log_path = std::path::Path::new("log/gnothi.log");
    if log_path.exists() {
        if let Ok(metadata) = fs::metadata(log_path) {
            if metadata.len() > 10 * 1024 * 1024 {
                let _ = fs::write(log_path, "");
            }
        }
    }

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(
            tauri_plugin_log::Builder::new()
                .target(tauri_plugin_log::Target::new(
                    tauri_plugin_log::TargetKind::Folder {
                        path: std::path::PathBuf::from("log"),
                        file_name: Some("gnothi".to_string()),
                    },
                ))
                .timezone_strategy(tauri_plugin_log::TimezoneStrategy::UseLocal)
                .level(log::LevelFilter::Info)
                .build(),
        )
        .setup(|_app| {
            info!("==================================================");
            info!("Gnothi 应用启动");
            info!("日志目录: ./log/gnothi.log");
            info!("数据库目录: ./data/gnothi.db");
            info!("==================================================");
            Ok(())
        })
        .manage(DbState {
            conn: Mutex::new({
                let conn = Connection::open("data/gnothi.db").expect("Failed to open database");
                info!("数据库连接成功");
                // 初始化表
                conn.execute_batch(
                    "CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT DEFAULT '',
                        created_at DATETIME,
                        updated_at DATETIME,
                        sort_order INTEGER DEFAULT 0
                    );
                    CREATE TABLE IF NOT EXISTS todos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        status TEXT DEFAULT 'pending',
                        priority TEXT DEFAULT 'medium',
                        due_date TEXT DEFAULT '',
                        notes TEXT DEFAULT '',
                        completed_at TEXT DEFAULT '',
                        created_at DATETIME,
                        updated_at DATETIME
                    );
                    CREATE TABLE IF NOT EXISTS daily_reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT UNIQUE NOT NULL,
                        columns TEXT DEFAULT '[]',
                        rows TEXT DEFAULT '[]',
                        created_at DATETIME,
                        updated_at DATETIME
                    );
                    CREATE INDEX IF NOT EXISTS idx_notes_sort_order ON notes(sort_order);
                    CREATE INDEX IF NOT EXISTS idx_daily_reports_date ON daily_reports(date);
                    CREATE TABLE IF NOT EXISTS mottos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        created_at DATETIME
                    );"
                ).expect("Failed to init database");
                
                // 插入默认名言（如果表为空）
                let count: i32 = conn.query_row("SELECT COUNT(*) FROM mottos", [], |row| row.get(0)).unwrap_or(0);
                if count == 0 {
                    let default_mottos = vec![
                        "工作是为了生活，而不是生活为了工作",
                        "上班一条虫，下班一条龙",
                        "摸鱼一时爽，一直摸鱼一直爽",
                        "工资是固定的，摸鱼就是赚到",
                        "今天也是充满希望的摸鱼日",
                        "再坚持一下，马上就自由了",
                        "只要心中有海，哪里都是马尔代夫",
                        "不是我想摸鱼，是鱼主动来找我的",
                        "世界上最远的距离，是上班到下班的距离",
                        "每天最重要的事情就是等下班",
                    ];
                    let now = chrono::Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
                    for motto in default_mottos {
                        conn.execute("INSERT INTO mottos (content, created_at) VALUES (?1, ?2)", params![motto, now]).ok();
                    }
                    info!("已插入默认名言");
                }
                
                conn
            }),
        })
        .invoke_handler(tauri::generate_handler![
            get_notes,
            get_note,
            create_note,
            update_note,
            delete_note,
            reorder_notes,
            get_todos,
            create_todo,
            update_todo,
            delete_todo,
            get_report_dates,
            get_report,
            save_report,
            delete_report,
            get_mottos,
            create_motto,
            update_motto,
            delete_motto,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
