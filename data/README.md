# Data

`sample_emails.csv` is a **tiny hand-written demo set (24 emails)** so the project runs out of the box.
It is only meant for smoke-testing the pipeline, not for real accuracy numbers.

For real training, place your full labelled dataset here as `data/Phishing_Email.csv` with columns:

| Column       | Values                          |
|--------------|---------------------------------|
| `Email Text` | raw email body                  |
| `Email Type` | `Phishing Email` / `Safe Email` |

Then run: `python train.py --data data/Phishing_Email.csv`
