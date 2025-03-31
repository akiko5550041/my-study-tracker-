import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import json
import uuid
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Meiryo'


# 保存先ディレクトリとファイル
SAVE_DIR = "records"
TAGS_FILE = os.path.join(SAVE_DIR, "tags.json")
RECORDS_FILE = os.path.join(SAVE_DIR, "records.csv")
os.makedirs(SAVE_DIR, exist_ok=True)

# タグ設定の読み書き
if not os.path.isfile(TAGS_FILE):
    with open(TAGS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

def load_tags():
    with open(TAGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tags(tags):
    with open(TAGS_FILE, "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)

TAGS = load_tags()

# 記録ファイル初期化
if not os.path.isfile(RECORDS_FILE):
    with open(RECORDS_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "日付", "正答率（％）", "タグ1", "タグ2", "タグ3", "タグ4", "メモ", "記録時間"])

# メインウィンドウ
root = tk.Tk()
root.title("学習手帳ツール（正答率・タグ4階層対応）")
root.geometry("800x650")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# ============ 記録ページ ============ （省略せず続く）...
# 記録ページ
frame_record = ttk.Frame(notebook)
notebook.add(frame_record, text='📘 記録')

tk.Label(frame_record, text="📅 日付 (YYYY-MM-DD)").pack()
entry_date = tk.Entry(frame_record)
entry_date.insert(0, datetime.today().strftime("%Y-%m-%d"))
entry_date.pack()

tk.Label(frame_record, text="🎯 正答率（％）").pack()
accuracy_options = [str(i) for i in range(0, 101, 5)]
combo_accuracy = ttk.Combobox(frame_record, values=accuracy_options, state="readonly")
combo_accuracy.set("0")
combo_accuracy.pack()

tk.Label(frame_record, text="🏷️ タグ1").pack()
combo_tag1 = ttk.Combobox(frame_record, values=list(TAGS.keys()), state="readonly")
combo_tag1.pack()

tk.Label(frame_record, text="🔖 タグ2").pack()
combo_tag2 = ttk.Combobox(frame_record, state="readonly")
combo_tag2.pack()

tk.Label(frame_record, text="🧩 タグ3").pack()
combo_tag3 = ttk.Combobox(frame_record, state="readonly")
combo_tag3.pack()

tk.Label(frame_record, text="🧷 タグ4").pack()
combo_tag4 = ttk.Combobox(frame_record, state="readonly")
combo_tag4.pack()

def update_tag2_options(event):
    t1 = combo_tag1.get()
    tag2_dict = TAGS.get(t1, {})
    combo_tag2["values"] = list(tag2_dict.keys()) if isinstance(tag2_dict, dict) else []
    combo_tag2.set("")
    combo_tag3.set("")
    combo_tag4.set("")
    combo_tag3["values"] = []
    combo_tag4["values"] = []

def update_tag3_options(event):
    t1, t2 = combo_tag1.get(), combo_tag2.get()
    tag3_dict = TAGS.get(t1, {}).get(t2, {})
    combo_tag3["values"] = list(tag3_dict.keys()) if isinstance(tag3_dict, dict) else []
    combo_tag3.set("")
    combo_tag4.set("")
    combo_tag4["values"] = []

def update_tag4_options(event):
    t1, t2, t3 = combo_tag1.get(), combo_tag2.get(), combo_tag3.get()
    tag4_list = TAGS.get(t1, {}).get(t2, {}).get(t3, [])
    combo_tag4["values"] = tag4_list if isinstance(tag4_list, list) else []
    combo_tag4.set("")

combo_tag1.bind("<<ComboboxSelected>>", update_tag2_options)
combo_tag2.bind("<<ComboboxSelected>>", update_tag3_options)
combo_tag3.bind("<<ComboboxSelected>>", update_tag4_options)

tk.Label(frame_record, text="📝 メモ").pack()
memo_text = tk.Text(frame_record, height=6, width=60)
memo_text.pack()

tk.Label(frame_record, text="🕒 記録時間（時:分）").pack()
entry_time = tk.Entry(frame_record)
entry_time.insert(0, datetime.now().strftime("%H:%M"))
entry_time.pack()

def save_record():
    uid = str(uuid.uuid4())
    values = [
        uid,
        entry_date.get(),
        combo_accuracy.get(),
        combo_tag1.get(),
        combo_tag2.get(),
        combo_tag3.get(),
        combo_tag4.get(),
        memo_text.get("1.0", tk.END).strip(),
        entry_time.get()
    ]
    if not values[1]:
        messagebox.showerror("エラー", "日付は必須です。")
        return
    with open(RECORDS_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(values)
    messagebox.showinfo("保存完了", "記録を保存しました。")
    load_records()
    entry_date.delete(0, tk.END)
    entry_date.insert(0, datetime.today().strftime("%Y-%m-%d"))
    combo_accuracy.set("0")
    combo_tag1.set("")
    combo_tag2.set("")
    combo_tag3.set("")
    combo_tag4.set("")
    memo_text.delete("1.0", tk.END)
    entry_time.delete(0, tk.END)
    entry_time.insert(0, datetime.now().strftime("%H:%M"))

tk.Button(frame_record, text="保存する", command=save_record).pack(pady=5)
# ============ タグ登録ページ ============

def update_filter_tag_options():
    combo_filter_tag1["values"] = list(TAGS.keys())
    combo_filter_tag2.set("")
    combo_filter_tag2["values"] = []
    combo_filter_tag3.set("")
    combo_filter_tag3["values"] = []
    combo_filter_tag4.set("")
    combo_filter_tag4["values"] = []



frame_tags = ttk.Frame(notebook)
notebook.add(frame_tags, text='🏷️ タグ登録')

# 追加用エントリー
tk.Label(frame_tags, text="タグ1（ジャンル）").pack()
entry_tag1 = tk.Entry(frame_tags)
entry_tag1.pack()

tk.Label(frame_tags, text="タグ2（トピック）").pack()
entry_tag2 = tk.Entry(frame_tags)
entry_tag2.pack()

tk.Label(frame_tags, text="タグ3（サブトピック）").pack()
entry_tag3 = tk.Entry(frame_tags)
entry_tag3.pack()

tk.Label(frame_tags, text="タグ4（詳細トピック）").pack()
entry_tag4 = tk.Entry(frame_tags)
entry_tag4.pack()

# タグ追加処理
def add_tag():
    t1, t2, t3, t4 = entry_tag1.get(), entry_tag2.get(), entry_tag3.get(), entry_tag4.get()
    if not t1 or not t2:
        messagebox.showerror("エラー", "タグ1とタグ2は必須です。")
        return
    if t1 not in TAGS:
        TAGS[t1] = {}
    if t2 not in TAGS[t1]:
        TAGS[t1][t2] = {}
    if t3 not in TAGS[t1][t2]:
        TAGS[t1][t2][t3] = []
    if t4 and t4 not in TAGS[t1][t2][t3]:
        TAGS[t1][t2][t3].append(t4)
    save_tags(TAGS)
    combo_tag1["values"] = list(TAGS.keys())
    update_filter_tag_options()
    delete_tag1["values"] = list(TAGS.keys())  # 削除コンボも更新
    messagebox.showinfo("追加完了", "タグを登録しました。")

# 削除用プルダウン
tk.Label(frame_tags, text="削除するタグ1").pack()
delete_tag1 = ttk.Combobox(frame_tags, values=list(TAGS.keys()), state="readonly")
delete_tag1.pack()

tk.Label(frame_tags, text="削除するタグ2").pack()
delete_tag2 = ttk.Combobox(frame_tags, state="readonly")
delete_tag2.pack()

tk.Label(frame_tags, text="削除するタグ3").pack()
delete_tag3 = ttk.Combobox(frame_tags, state="readonly")
delete_tag3.pack()

tk.Label(frame_tags, text="削除するタグ4").pack()
delete_tag4 = ttk.Combobox(frame_tags, state="readonly")
delete_tag4.pack()

# 階層連動（削除用）
def update_delete_tag2(event):
    t1 = delete_tag1.get()
    delete_tag2["values"] = list(TAGS.get(t1, {}).keys())
    delete_tag2.set("")
    delete_tag3.set("")
    delete_tag3["values"] = []
    delete_tag4.set("")
    delete_tag4["values"] = []

def update_delete_tag3(event):
    t1, t2 = delete_tag1.get(), delete_tag2.get()
    delete_tag3["values"] = list(TAGS.get(t1, {}).get(t2, {}).keys())
    delete_tag3.set("")
    delete_tag4.set("")
    delete_tag4["values"] = []

def update_delete_tag4(event):
    t1, t2, t3 = delete_tag1.get(), delete_tag2.get(), delete_tag3.get()
    delete_tag4["values"] = TAGS.get(t1, {}).get(t2, {}).get(t3, [])
    delete_tag4.set("")

delete_tag1.bind("<<ComboboxSelected>>", update_delete_tag2)
delete_tag2.bind("<<ComboboxSelected>>", update_delete_tag3)
delete_tag3.bind("<<ComboboxSelected>>", update_delete_tag4)

# タグ削除処理
def delete_tag():
    t1, t2, t3, t4 = delete_tag1.get(), delete_tag2.get(), delete_tag3.get(), delete_tag4.get()
    try:
        if t4 and t3 in TAGS.get(t1, {}).get(t2, {}):
            TAGS[t1][t2][t3].remove(t4)
            if not TAGS[t1][t2][t3]:
                del TAGS[t1][t2][t3]
        elif t3 and t3 in TAGS.get(t1, {}).get(t2, {}):
            del TAGS[t1][t2][t3]
        elif t2 and t2 in TAGS.get(t1, {}):
            del TAGS[t1][t2]
        elif t1 and t1 in TAGS:
            del TAGS[t1]
        save_tags(TAGS)
        combo_tag1["values"] = list(TAGS.keys())
        update_filter_tag_options()
        delete_tag1["values"] = list(TAGS.keys())
        messagebox.showinfo("削除完了", "タグを削除しました。")
    except Exception as e:
        messagebox.showerror("削除エラー", f"削除できませんでした: {e}")

tk.Button(frame_tags, text="タグを追加する", command=add_tag).pack(pady=5)
tk.Button(frame_tags, text="タグを削除する", command=delete_tag).pack(pady=5)
# ===== アウトプットページタブ =====
frame_output = ttk.Frame(notebook)
notebook.add(frame_output, text='📊 アウトプット')

# ===== フィルターUI =====
filter_frame = ttk.Frame(frame_output)
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="タグ1:").grid(row=0, column=0)
combo_filter_tag1 = ttk.Combobox(filter_frame, state="readonly")
combo_filter_tag1.grid(row=0, column=1)

tk.Label(filter_frame, text="タグ2:").grid(row=0, column=2)
combo_filter_tag2 = ttk.Combobox(filter_frame, state="readonly")
combo_filter_tag2.grid(row=0, column=3)

tk.Label(filter_frame, text="タグ3:").grid(row=1, column=0)
combo_filter_tag3 = ttk.Combobox(filter_frame, state="readonly")
combo_filter_tag3.grid(row=1, column=1)

tk.Label(filter_frame, text="タグ4:").grid(row=1, column=2)
combo_filter_tag4 = ttk.Combobox(filter_frame, state="readonly")
combo_filter_tag4.grid(row=1, column=3)

tk.Label(filter_frame, text="正答率:").grid(row=2, column=0)
entry_filter_accuracy = tk.Entry(filter_frame)
entry_filter_accuracy.grid(row=2, column=1)

tk.Label(filter_frame, text="フィルタタイプ:").grid(row=2, column=2)
combo_filter_type = ttk.Combobox(filter_frame, values=["以上", "以下"], state="readonly")
combo_filter_type.set("以上")
combo_filter_type.grid(row=2, column=3)

# ===== タグ連動バインド =====
def update_filter_tag2(event):
    t1 = combo_filter_tag1.get()
    combo_filter_tag2["values"] = list(TAGS.get(t1, {}).keys())
    combo_filter_tag2.set("")
    combo_filter_tag3.set("")
    combo_filter_tag3["values"] = []
    combo_filter_tag4.set("")
    combo_filter_tag4["values"] = []

def update_filter_tag3(event):
    t1, t2 = combo_filter_tag1.get(), combo_filter_tag2.get()
    combo_filter_tag3["values"] = list(TAGS.get(t1, {}).get(t2, {}).keys())
    combo_filter_tag3.set("")
    combo_filter_tag4.set("")
    combo_filter_tag4["values"] = []

def update_filter_tag4(event):
    t1, t2, t3 = combo_filter_tag1.get(), combo_filter_tag2.get(), combo_filter_tag3.get()
    combo_filter_tag4["values"] = TAGS.get(t1, {}).get(t2, {}).get(t3, [])
    combo_filter_tag4.set("")

combo_filter_tag1.bind("<<ComboboxSelected>>", update_filter_tag2)
combo_filter_tag2.bind("<<ComboboxSelected>>", update_filter_tag3)
combo_filter_tag3.bind("<<ComboboxSelected>>", update_filter_tag4)

# ===== TreeView =====
columns = ["ID", "日付", "正答率（％）", "タグ1", "タグ2", "タグ3", "タグ4", "メモ", "記録時間"]
tree = ttk.Treeview(frame_output, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill=tk.BOTH, expand=True)

# ===== 標準表示 =====
def load_records():
    tree.delete(*tree.get_children())
    if not os.path.isfile(RECORDS_FILE):
        return
    with open(RECORDS_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            tree.insert("", tk.END, values=row[:8])

# ===== 最新のみ色付き表示 =====
def load_latest_records():
    latest = {}
    if not os.path.isfile(RECORDS_FILE):
        return []
    with open(RECORDS_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            key = tuple(row[3:7])
            dt = datetime.strptime(f"{row[1]} {row[8]}", "%Y-%m-%d %H:%M")
            if key not in latest or latest[key][0] < dt:
                latest[key] = (dt, row)
    return [v[1] for v in latest.values()]

def show_latest_records_with_colors():
    tree.delete(*tree.get_children())
    records = load_latest_records()
    for row in records:
        score = float(row[2])
        tag = 'red' if score < 80 else 'yellow'
        tree.insert("", tk.END, values=row[:8], tags=(tag,))
    tree.tag_configure('red', background='#ffcccc')
    tree.tag_configure('yellow', background='#ffffcc')

# ===== 折れ線グラフ（ダブルクリック） =====
def on_tree_item_click(event):
    selected = tree.selection()
    if not selected:
        return
    vals = tree.item(selected[0])["values"]
    selected_key = tuple(vals[3:7])

    data = []
    with open(RECORDS_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if tuple(row[3:7]) == selected_key:
                data.append(float(row[2]))

    if not data:
        return

    plt.figure()
    plt.plot(range(1, len(data)+1), data, marker='o')
    plt.title(f"タグ: {' > '.join(selected_key)} の成績推移")
    plt.xlabel("試行回数")
    plt.ylabel("正答率（％）")
    plt.xticks(range(1, len(data)+1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

tree.bind("<Double-1>", on_tree_item_click)

# ===== フィルタークリア =====
tk.Button(filter_frame, text="🔄 フィルターをクリア", command=lambda: [
    combo_filter_tag1.set(""), combo_filter_tag2.set(""),
    combo_filter_tag3.set(""), combo_filter_tag4.set(""),
    entry_filter_accuracy.delete(0, tk.END),
    load_records()
]).grid(row=4, column=0, columnspan=4, pady=5)

# ===== 進捗率を柔軟に計算（深さで判定） =====
def show_under_80_report():
    t1 = combo_filter_tag1.get()
    t2 = combo_filter_tag2.get()
    t3 = combo_filter_tag3.get()
    t4 = combo_filter_tag4.get()
    if not t1:
        messagebox.showwarning("未選択", "タグ①（テキスト名）を選んでください。")
        return

    # 母数取得（TAGSベース）
    def extract_keys_from_tags(tags, prefix=[]):
        results = []
        if isinstance(tags, dict):
            for k, v in tags.items():
                results += extract_keys_from_tags(v, prefix + [k])
        elif isinstance(tags, list):
            for item in tags:
                results.append(tuple(prefix + [item]))
        return results

    filtered_tags = TAGS.get(t1, {})
    if t2:
        filtered_tags = filtered_tags.get(t2, {})
    if t3:
        filtered_tags = filtered_tags.get(t3, {})
    if t4:
        filtered_tags = {t4: []}  # ダミー構造

    target_keys = extract_keys_from_tags(filtered_tags)
    if not target_keys:
        messagebox.showinfo("データなし", "該当する教材構造が存在しません。")
        return

    # 最新記録取得
    latest_scores = {}
    with open(RECORDS_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            key = tuple(row[3:7])
            dt = datetime.strptime(f"{row[1]} {row[8]}", "%Y-%m-%d %H:%M")
            if key not in latest_scores or latest_scores[key][0] < dt:
                latest_scores[key] = (dt, float(row[2]))

    under_80 = 0
    matched = 0
    for k in target_keys:
        full_key = (t1,) + tuple(k)
        score = latest_scores.get(full_key, (None, 0))[1]
        if full_key in latest_scores:
            matched += 1
            if score < 80:
                under_80 += 1

    percent = round((matched - under_80) / matched * 100, 1) if matched else 0
    messagebox.showinfo("📘 進捗レポート", f"進捗対象数（登録構造）: {len(target_keys)}\n"
                                       f"記録済み（最新記録）: {matched}\n"
                                       f"❌ 80点未満: {under_80} 項目\n"
                                       f"📊 完成率: {percent}%")

# ===== 削除関数（1件・まとめ） =====
def delete_record():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("選択なし", "削除する記録を選んでください。")
        return
    selected_id = tree.item(selected[0])["values"][0]
    new_rows = []
    with open(RECORDS_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] != selected_id:
                new_rows.append(row)
    with open(RECORDS_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(new_rows)
    messagebox.showinfo("削除完了", "記録を削除しました。")
    show_latest_records_with_colors()

def delete_all_records_for_selected_tag_confirmed():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("選択なし", "削除したいタグの行を選んでください。")
        return
    selected_values = tree.item(selected[0])['values']
    selected_tag = tuple(selected_values[3:7])
    matched_rows = []
    with open(RECORDS_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if tuple(row[3:7]) == selected_tag:
                matched_rows.append(row)
    count = len(matched_rows)
    if count == 0:
        messagebox.showinfo("削除対象なし", "該当タグの記録は見つかりませんでした。")
        return
    confirm = messagebox.askyesno("確認", f"タグ「{' > '.join(selected_tag)}」に該当する記録が {count} 件あります。\nすべて削除しますか？")
    if not confirm:
        return
    new_rows = []
    with open(RECORDS_FILE, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if tuple(row[3:7]) != selected_tag:
                new_rows.append(row)
    with open(RECORDS_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(new_rows)
    messagebox.showinfo("削除完了", f"{count} 件の記録を削除しました。")
    show_latest_records_with_colors()

# ===== ボタン類 =====
tk.Button(frame_output, text="📄 すべての記録を表示（標準）", command=load_records).pack(pady=3)
tk.Button(frame_output, text="📘 進捗状況を確認（80点未満）", command=show_under_80_report).pack(pady=3)
tk.Button(frame_output, text="🔍 最新記録だけ表示（色付き）", command=show_latest_records_with_colors).pack(pady=3)
tk.Button(frame_output, text="🗑 選択した記録を1件だけ削除", command=delete_record).pack(pady=3)
tk.Button(frame_output, text="🗑 同じタグの記録をまとめて削除", command=delete_all_records_for_selected_tag_confirmed).pack(pady=3)


# ===== タグフィルター初期化関数 =====
def update_filter_tag_options():
    combo_filter_tag1["values"] = list(TAGS.keys())
    combo_filter_tag1.set("")
    combo_filter_tag2.set("")
    combo_filter_tag2["values"] = []
    combo_filter_tag3.set("")
    combo_filter_tag3["values"] = []
    combo_filter_tag4.set("")
    combo_filter_tag4["values"] = []

# ===== 起動時に実行する =====
update_filter_tag_options()
load_records()


# メインループ開始
root.mainloop()


