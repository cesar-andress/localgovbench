# Synthetic municipality corpus

**50 fictional municipalities**, each with six Markdown governance documents.

| Item | Location |
|------|----------|
| Documents | `municipalities/mun_NNN_<slug>/` |
| Metadata | `metadata.json` |
| Generation assumptions | [docs/synthetic_municipality_corpus.md](../../docs/synthetic_municipality_corpus.md) |

Regenerate:

```bash
python scripts/generate_municipality_corpus.py
```

All content is **synthetic** — not empirical municipal data.
