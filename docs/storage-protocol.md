# Fast-play persistence: GitHub canonical, Notion projection

- GitHub main: single current numeric snapshot at state/current.json, immutable event history in events/, NPC/world lore in canon/, imported evidence in sources/drive/.
- Notion: read-optimized index of changed NPCs, quests and latest checkpoint. Store last_synced_commit_sha; do not override GitHub canon.
- During normal gameplay: resolve turns in ChatGPT; track deltas locally in the chat. Flush to GitHub every 5 turns maximum, on major NPC/quest event, before moving chats, or on user demand (whichever first).
- Each flush: read head -> resolve delta -> check arithmetic/causality -> commit with expected-head guard -> fetch/read-back -> update Notion projection. On write failure, distinguish UNSAVED delta from canonical state.
- **No automatic ingestion or background timer is currently configured.** A scheduled reminder alone cannot access new chat turn events.
- Special invariants: Edran=Tư Tế Xương, Maela hunter, Kharzug old Tam Nha war beast NOT Huyết Lang Độc Nhãn killed T66, unnamed pup safe T93; no arbitrary deaths/teleports; Cam Lao gate still sealed; Tam Trao tripwire bypassed not disarmed; no boss loot double count after accepted replay.
- Repo is PUBLIC by explicit owner approval. Do not add real-world secrets, credentials or unrelated personal records.
- Drive folder remains available for provenance; do not delete or rewrite it automatically.
