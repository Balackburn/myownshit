# Review and render-queue tools

These scripts drive the draft → review → correction loop of the stories. They were written in the session's scratch directory and are kept here so
they survive it. Several of them hold the scratch path in a variable `SP` at the top: set it to your own working directory before use.

| File | What it does |
| --- | --- |
| `runq4.sh` | Fair render queue: one ticket per waiting job, the oldest live ticket starts when fewer than three renders run. |
| `runqP.sh` | Priority lane (stills and finals), limit four renders. |
| `runq3.sh` | The old queue (random order between waiters); kept for reference, do not use. |
| `renice_drafts.sh` | Lowers the priority of the running drafts. |
| `qa.sh` | Final checks of a delivered film (size, frame rate, loudness, grey frames). |
| `next_config.py` | Writes the config of review round N+1 from round N (strip groups `S11_S13` are expanded to S11, S12, S13). |
| `make_critic.py` | Builds a review folder from a config: brief, evidence list, the two critics' prompts, `build.sh`. Needs `template/`. |
| `critic_final.py`, `critic_final_stills.sh` | Extract the stills and strips of the draft the critics look at. |
| `shot_strips.py`, `critic_motion.py`, `dsheet.py` | Contact strips per shot, frame-to-frame motion measure, labelled contact sheets. |
| `save_report.py` | Saves a critic's report from an agent's output file. |
| `review_draft_workflow.js` | Workflow script: two independent critics (animation director, art director) read a review folder and return a score and a report each. Arguments: `{name, round, folder}`. |
| `template/` | The critics' standing instructions and the style reference image copied into every review folder. |
