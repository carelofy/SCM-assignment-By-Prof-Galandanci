import datetime
import json
from pathlib import Path


class Book:
    def __init__(self, isbn, title, author, copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies

    def to_dict(self):
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(data["isbn"], data["title"], data["author"], data["total_copies"])
        book.available_copies = data["available_copies"]
        return book


class Member:
    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_books = {}
        self.fines = 0.0

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "borrowed_books": {
                isbn: due.isoformat() for isbn, due in self.borrowed_books.items()
            },
            "fines": self.fines
        }

    @classmethod
    def from_dict(cls, data):
        member = cls(data["member_id"], data["name"], data["email"])
        member.borrowed_books = {
            isbn: datetime.date.fromisoformat(due_date)
            for isbn, due_date in data.get("borrowed_books", {}).items()
        }
        member.fines = float(data.get("fines", 0.0))
        return member


class Library:
    FINE_PER_DAY = 0.5
    LOAN_PERIOD_DAYS = 14

    def __init__(self):
        self.books = {}
        self.members = {}

    def add_book(self, isbn, title, author, copies=1):
        if isbn in self.books:
            self.books[isbn].total_copies += copies
            self.books[isbn].available_copies += copies
        else:
            self.books[isbn] = Book(isbn, title, author, copies)
        return self.books[isbn]

    def register_member(self, member_id, name, email):
        if member_id in self.members:
            raise ValueError("Member already exists")
        member = Member(member_id, name, email)
        self.members[member_id] = member
        return member

    def borrow_book(self, member_id, isbn):
        if member_id not in self.members:
            raise ValueError("Unknown member")
        if isbn not in self.books:
            raise ValueError("Unknown book")

        member = self.members[member_id]
        book = self.books[isbn]

        if book.available_copies <= 0:
            raise RuntimeError("No copies available")
        if isbn in member.borrowed_books:
            raise RuntimeError("Member already has this book")
        if member.fines > 5:
            raise RuntimeError("Outstanding fines too high to borrow")

        due_date = datetime.date.today() + datetime.timedelta(days=self.LOAN_PERIOD_DAYS)
        member.borrowed_books[isbn] = due_date
        book.available_copies -= 1
        return due_date

    def return_book(self, member_id, isbn, return_date=None):
        if member_id not in self.members:
            raise ValueError("Unknown member")
        member = self.members[member_id]

        if isbn not in member.borrowed_books:
            raise RuntimeError("Member did not borrow this book")

        if return_date is None:
            return_date = datetime.date.today()

        due_date = member.borrowed_books.pop(isbn)
        book = self.books[isbn]
        book.available_copies += 1

        late_days = (return_date - due_date).days
        fine = 0.0
        if late_days > 0:
            fine = late_days * self.FINE_PER_DAY
            member.fines += fine

        return fine

    def pay_fine(self, member_id, amount):
        if member_id not in self.members:
            raise ValueError("Unknown member")
        member = self.members[member_id]
        if amount <= 0:
            raise ValueError("Payment must be positive")
        member.fines = max(0.0, member.fines - amount)
        return member.fines

    def search_by_title(self, keyword):
        keyword = keyword.lower()
        return [b for b in self.books.values() if keyword in b.title.lower()]

    def search_by_author(self, keyword):
        keyword = keyword.lower()
        return [b for b in self.books.values() if keyword in b.author.lower()]

    def overdue_members(self):
        today = datetime.date.today()
        overdue = []
        for member in self.members.values():
            for isbn, due in member.borrowed_books.items():
                if due < today:
                    overdue.append((member.member_id, isbn, (today - due).days))
        return overdue

    def export_state(self, filepath):
        state = {
            "books": [b.to_dict() for b in self.books.values()],
            "members": [m.to_dict() for m in self.members.values()]
        }
        with open(filepath, "w") as f:
            json.dump(state, f, indent=2)

    def load_state(self, filepath):
        """Restore previously exported books and members from a JSON state file."""
        with open(filepath, "r") as f:
            state = json.load(f)

        self.books = {
            data["isbn"]: Book.from_dict(data)
            for data in state.get("books", [])
        }
        self.members = {
            data["member_id"]: Member.from_dict(data)
            for data in state.get("members", [])
        }
        return len(self.books), len(self.members)


def demo():
    lib = Library()
    state_file = Path("library_state.json")

    if state_file.exists():
        books, members = lib.load_state(state_file)
        print(f"Loaded saved state: {books} books, {members} members")
        return

    lib.add_book("111", "Clean Code", "Robert C. Martin", 2)
    lib.add_book("222", "The Pragmatic Programmer", "Andrew Hunt", 1)
    lib.register_member("M1", "Ada Lovelace", "ada@example.com")
    lib.register_member("M2", "Alan Turing", "alan@example.com")

    due = lib.borrow_book("M1", "111")
    print("M1 borrowed 111, due", due)

    fine = lib.return_book("M1", "111", return_date=due + datetime.timedelta(days=3))
    print("Late fine charged:", fine)

    results = lib.search_by_title("clean")
    print("Search results:", [b.title for b in results])

    lib.export_state(state_file)
    print(f"Saved library state to {state_file}")


if __name__ == "__main__":
    demo()
