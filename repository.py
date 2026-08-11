import os
import psycopg2
from psycopg2.extras import RealDictCursor
from models import Contact

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "contacts"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASS", "mypassword123"),
        port=os.getenv("DB_PORT", "5432"),
    )

class ContactRepository:
    def find_all(self) -> list[Contact]:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM contacts ORDER BY id DESC")
                rows = cur.fetchall()
                return [Contact(**row) for row in rows]

    def find_by_id(self, contact_id: int) -> Contact | None:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM contacts WHERE id = %s", (contact_id,))
                row = cur.fetchone()
                return Contact(**row) if row else None

    def create(self, contact: Contact) -> Contact:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO contacts (name, email, phone, company)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (contact.name, contact.email, contact.phone, contact.company),
                )
                contact.id = cur.fetchone()[0]
                conn.commit()
                return contact

    def update(self, contact: Contact) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE contacts
                    SET name = %s, email = %s, phone = %s, company = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (contact.name, contact.email, contact.phone, contact.company, contact.id),
                )
                conn.commit()
                return cur.rowcount > 0

    def delete(self, contact_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
                conn.commit()
                return cur.rowcount > 0