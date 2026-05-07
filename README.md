# OS-CEP

Short producer–consumer simulation using threads in Python.

Purpose: Demonstrates synchronization between multiple `Picker` threads (producers)
and a `Loader` thread (consumer). Pickers remove items from a shared `tree`
and place them into a fixed-size `crate`; the Loader moves full crates to the `truck`.

Key components:
- `Picker(pid)`: picks fruits from `tree`, waits for crate space, appends to `crate`.
- `Loader()`: waits for `crate_full`, moves crate contents to `truck`, frees slots.
- Sync primitives: `mutex_tree`, `mutex_crate` (Locks); `crate_empty`, `crate_full` (Semaphores).
- Config: `CRATE_SIZE` (default 12) and a small `time.sleep` in pickers.

Run:
```bash
python spring_workers.py
```

Output: console logs showing pick actions, crate loads, and final `truck` contents.