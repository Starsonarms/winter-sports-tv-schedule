# MongoDB Configuration

## Dedicated MongoDB Atlas Cluster

This project has its own dedicated MongoDB Atlas cluster:

- **Cluster**: `wintersportsreminders.y80xoa0.mongodb.net`
- **Username**: `palmchristian_db_admin`
- **Database**: `winter_sports`

## Benefits

✅ **Dedicated resources** - separate cluster for winter sports reminders  
✅ **Free tier** - no additional costs  
✅ **Isolated data** - completely separate from other projects  
✅ **Scalable** - can grow independently

## Collections Created

The reminder system creates these collections in the `winter_sports` database:

- **`sent_reminders`** - Tracks which reminders have been sent
  - Prevents duplicate notifications
  - Automatically cleans up old entries (7 days)
  - Indexed on `event_id` and `minutes_before` for fast lookups

## Database Structure

```
MongoDB Atlas Cluster: wintersportsreminders.y80xoa0.mongodb.net
└── winter_sports (winter sports reminders database)
    └── sent_reminders
        ├── event_id (string)
        ├── event_title (string)
        ├── minutes_before (int: 60, 15, etc.)
        ├── event_datetime (datetime)
        └── sent_at (datetime)
```

## Indexes

The following indexes are automatically created:

1. **Compound Unique Index**: `event_id + minutes_before`
   - Prevents duplicate reminders for the same event
   - Ensures only one 60-min and one 15-min reminder per event

2. **Single Index**: `event_datetime`
   - Used for cleanup queries
   - Efficiently finds old reminders to delete

3. **Sorted Index**: `sent_at` (descending)
   - Used for displaying recent reminders
   - Optimizes "last N reminders" queries

## Configuration

Your `.env` file should have:

```bash
# MongoDB Settings
MONGODB_URI=mongodb+srv://palmchristian_db_admin:jIk9RizuxOLxtWDW@wintersportsreminders.y80xoa0.mongodb.net/?appName=wintersportsreminders
MONGODB_DATABASE=winter_sports
```

These settings are already in `.env.example` - just copy them to `.env`.

## Initialize Collections

After setting up your `.env` file, initialize the database:

```bash
python manage.py init-db
```

This creates the `sent_reminders` collection and all necessary indexes.

## Testing

Test your MongoDB connection:

```bash
python manage.py test-mongodb
```

Expected output:
```
=== Testing MongoDB Connection ===

MongoDB Cluster: wintersportsreminders.y80xoa0.mongodb.net (MongoDB Atlas)
Database: winter_sports
URI Configured: ✅ Yes

✅ Successfully connected to MongoDB

=== Recent Reminders (0) ===

No reminders sent yet
```

## Viewing Data in MongoDB Atlas

1. Go to [cloud.mongodb.com](https://cloud.mongodb.com)
2. Sign in with your account
3. Select the `wintersportsreminders` cluster
4. Click "Browse Collections"
5. You'll see the `winter_sports` database with:
   - `sent_reminders` collection

## What Happens Without MongoDB?

If MongoDB connection fails, the reminder system will still work, but:

⚠️ You might receive duplicate reminders  
⚠️ No persistent tracking of sent notifications  

The system will log a warning and continue operating.

## Troubleshooting

### Connection Failed

If you see "MongoDB connection failed":

1. Check that credentials in `.env` match `.env.example`
2. Verify internet connection (MongoDB Atlas is cloud-based)
3. Check MongoDB Atlas dashboard for cluster status
4. Ensure cluster allows connections from your IP

### URI Format Issues?

The MongoDB URI should be exactly:
```
mongodb+srv://palmchristian_db_admin:jIk9RizuxOLxtWDW@wintersportsreminders.y80xoa0.mongodb.net/?appName=wintersportsreminders
```

Make sure:
- No spaces in the URI
- Username and password are correct (no typos)
- The `@` symbol separates credentials from cluster address
- The cluster name is `wintersportsreminders.y80xoa0.mongodb.net`
