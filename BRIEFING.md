# Hackathon IBM Bob 2.0 — Project Briefing & MVP Spec

Dokumen briefing resmi dan arsitektur teknis untuk proyek Hackathon IBM Bob 2.0: **Automated Real-Time Kanban Board with Evidence Links & watsonx.ai**.

---

## 1. Fitur Wajib (Core MVP — Wajib Demo)

| # | Fitur | Kenapa Wajib |
|---|---|---|
| **1** | **Auto-create kartu dari PR/branch baru** | Diferensiator utama, "wow moment" utama di demo. |
| **2** | **Auto-update status kartu** (PR opened → *In Progress*, PR merged → *Done*) | Bukti board "update sendiri" secara real-time. |
| **3** | **Setiap kartu ada link bukti** (link ke PR/commit terkait) | Janji utama di pitch: *"lengkap dengan bukti"*. |
| **4** | **Chat-based manual card creation** | Fallback kalau AI auto-detect gagal, cepat dibangun (prompt → structured extract). |
| **5** | **Dashboard board (Kanban view)** | Wajib visual demo: React dengan 3 kolom (*To Do*, *In Progress*, *Done*). |

---

## 2. Fitur Bonus (Stretch Goals)

| # | Fitur | Effort | Catatan & Strategi |
|---|---|---|---|
| **6** | **Alarm PR diam >2 hari** | Medium | Scheduled cron job / background check, logic sederhana. |
| **7** | **Dokumen (PDF) → kartu otomatis** | Medium | Parsing spesifikasi PDF menjadi checklist kartu tugas. |
| **8** | **Scope-creep warning** (diff 3x estimasi) | Medium | Baseline estimasi awal vs LOC diff aktual. |
| **9** | **Test-fail detection** (CI integration) | Tinggi & rapuh | Rekomendasi: siapkan simulated demo payload / rig CI. |
| **10** | **AI auto-assign & auto-estimate** | Rendah-Medium | Extracted prompt saat PR dibuat untuk tebak assignee & estimasi story points/jam. |

---

## 3. Alur Penggunaan User (User Flow)

### Skenario 1 — Setup Awal (PM/Team Lead)
1. PM login/register di dashboard.
2. Hubungkan repository GitHub (install GitHub App atau masukkan webhook URL ke repo settings).
3. Sistem mendengarkan event repo secara otomatis, board siap dipakai.

### Skenario 2 — Developer Kerja Normal (Fitur Wajib #1 & #2)
1. Developer membuat branch baru atau membuka Pull Request di GitHub (aktivitas reguler, tanpa friksi).
2. Webhook GitHub terpicu ke backend FastAPI.
3. AI watsonx membaca commit message & deskripsi PR → membuat kartu otomatis (judul, deskripsi, assignee, tipe task, estimasi).
4. Kartu muncul di dashboard React pada kolom **"In Progress"** lengkap dengan link bukti ke PR.
5. Push commit baru → info commit otomatis ditambahkan ke riwayat bukti kartu.
6. Developer merge PR → webhook terpicu → kartu otomatis berpindah ke **"Done"**.

### Skenario 3 — PM Bikin Kartu Manual via Chat (Fitur Wajib #4)
1. PM membuka widget chat di dashboard.
2. PM mengetik instruksi bebas, misal: *"buat kartu: refactor auth module, assign ke Firza, deadline Jumat"*.
3. AI mengekstrak data menjadi kartu terstruktur (Title, Description, Assignee, Due Date) dan mengecek korelasi branch/PR jika ada.
4. Kartu otomatis masuk ke kolom **"To Do"**.

### Skenario 4 — PM Cek Progress Tim (Value Utama)
1. PM membuka dashboard dan langsung melihat Kanban board yang selalu up-to-date.
2. Klik kartu manapun → melihat detail lengkap + tautan bukti langsung ke commit/PR GitHub.
3. Melihat indikator visual (badge peringatan jika PR stale atau scope creep).
4. Tidak ada lagi pertanyaan manual *"Progress-nya udah sampai mana?"*.

---

## 4. Struktur Folder Project

```text
.
├── backend/
│   ├── app/
│   │   ├── main.py                          # Entry point FastAPI
│   │   ├── config.py                        # Config & env vars (watsonx, GitHub, DB)
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── routes_webhook.py        # POST /webhook/github (terima event PR/push)
│   │   │       ├── routes_cards.py          # CRUD kartu (GET/PUT/DELETE)
│   │   │       ├── routes_chat.py           # POST /chat (manual card creation via chat)
│   │   │       └── routes_board.py          # GET /board (ambil semua kartu buat dashboard)
│   │   ├── core/
│   │   │   ├── github/
│   │   │   │   ├── webhook_handler.py       # parse payload webhook GitHub
│   │   │   │   ├── github_client.py         # GitHub API client (fetch PR detail, commit)
│   │   │   │   └── event_router.py          # routing event ke handler
│   │   │   ├── ai/
│   │   │   │   ├── card_generator.py        # LLM: PR/commit → structured card
│   │   │   │   ├── chat_parser.py           # LLM: chat text → structured card
│   │   │   │   ├── doc_parser.py            # (bonus) PDF spec → list of cards
│   │   │   │   └── watsonx_client.py        # koneksi ke IBM watsonx.ai
│   │   │   ├── scheduler/
│   │   │   │   └── stale_pr_checker.py      # (bonus) cron cek PR diam >2 hari
│   │   │   └── scoring/
│   │   │       └── estimation.py            # hitung estimasi dari diff code
│   │   ├── models/
│   │   │   ├── schemas.py                   # Pydantic schemas
│   │   │   └── db_models.py                 # SQLAlchemy DB models
│   │   ├── services/
│   │   │   ├── card_service.py              # business logic kartu
│   │   │   └── board_service.py             # aggregate data board
│   │   └── db/
│   │       ├── database.py                  # koneksi DB (SQLite/Postgres)
│   │       └── migrations/
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
└── frontend/
    ├── src/
    │   ├── main.jsx
    │   ├── App.jsx
    │   ├── router.jsx
    │   ├── pages/
    │   │   ├── OnboardingPage.jsx           # connect repo GitHub
    │   │   ├── BoardPage.jsx                # Kanban board utama
    │   │   ├── CardDetailPage.jsx           # detail kartu & bukti
    │   │   └── ChatPage.jsx                 # chat widget / drawer
    │   ├── components/
    │   │   ├── layout/
    │   │   │   ├── Navbar.jsx
    │   │   │   └── Sidebar.jsx
    │   │   ├── board/
    │   │   │   ├── KanbanBoard.jsx          # wrapper 3 kolom (To Do/In Progress/Done)
    │   │   │   ├── KanbanColumn.jsx
    │   │   │   ├── TaskCard.jsx
    │   │   │   ├── EvidenceLink.jsx         # badge link ke PR/commit
    │   │   │   └── AlarmBadge.jsx           # badge alarm
    │   │   ├── chat/
    │   │   │   ├── ChatBox.jsx
    │   │   │   └── ChatMessage.jsx
    │   │   └── common/
    │   │       ├── Button.jsx
    │   │       ├── Modal.jsx
    │   │       └── Loader.jsx
    │   ├── services/
    │   │   └── api.js                       # Axios HTTP client
    │   ├── hooks/
    │   │   ├── useBoard.js
    │   │   └── useChat.js
    │   └── styles/
    │       └── globals.css
    ├── package.json
    └── vite.config.js
```

---

## 5. Rencana Eksekusi & Demo Resilience Strategy

1. **Dual Mode watsonx.ai (Live + Resilient Mock Fallback)**:
   - Menggunakan IBM watsonx.ai API dengan prompt terstruktur (JSON schema).
   - Menyediakan deterministic fallback parser agar saat demo di panggung hackathon, aplikasi **100% tahan banting** dari kendala koneksi atau token limit.
2. **Demo Webhook Simulator**:
   - Selain webhook GitHub publik (via ngrok/smee.io), backend dilengkapi endpoint simulasi (`/api/v1/demo/simulate-pr-open`, `/simulate-pr-merge`, dll.) agar juri bisa langsung menyaksikan perpindahan kartu real-time dalam hitungan detik.
3. **Evidence Badging**:
   - Setiap kartu menyimpan relasi link ke PR GitHub, nomor PR, status commit hash, dan avatar pembuat PR.
