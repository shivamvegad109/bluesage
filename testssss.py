# open sqlite database

from datetime import datetime
import sqlite3
# D:\Django-Ui-eommerce\UI\django-ecommerce\db.sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
# auth_user remove id 2 data
# c.execute("DELETE FROM auth_user WHERE id=3")
# conn.commit()
# conn.close()

# alter table Order add created_at = models.DateTimeField(auto_now_add=True) updated_at = models.DateTimeField(auto_now=True)

# c.execute("ALTER TABLE shop_order ADD COLUMN created_at DATETIME")
# conn.commit()
# conn.close()
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Update existing rows with the current timestamp
current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
c.execute("UPDATE shop_order SET created_at = ?", (current_timestamp,))

# Commit the changes
conn.commit()

# Close the connection
conn.close()