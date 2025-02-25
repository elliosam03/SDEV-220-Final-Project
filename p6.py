import tkinter as tk
from tkinter import messagebox

#Classes for the Program
class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.borrowed_books = {}

    def add_book(self, book):
        self.books.append(book)

    def register_member(self, member):
        self.members.append(member)

    def borrow_book(self, member_id, book_id):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.book_id == book_id and not b.is_borrowed), None)
        
        if member and book:
            if member.borrow_book(book):
                self.borrowed_books.setdefault(member_id, []).append(book)
                return book.title
        return None
    
    def return_book(self, member_id, book_id):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.book_id == book_id), None)
        
        if member and book and book in member.borrowed_books:
            if member.return_book(book):
                self.borrowed_books[member_id].remove(book)
                if not self.borrowed_books[member_id]:
                    del self.borrowed_books[member_id]
                return True
        return False
    
    def view_available_books(self):
        return [book for book in self.books if not book.is_borrowed]
    
    def view_members(self):
        return self.members

class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = False
    
    def borrow_book(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            return True
        return False
    
    def return_book(self):
        if self.is_borrowed:
            self.is_borrowed = False
            return True
        return False

class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []
    
    def borrow_book(self, book):
        if book.borrow_book():
            self.borrowed_books.append(book)
            return True
        return False
    
    def return_book(self, book):
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            return True
        return False

# Library Management System Application via Tkinter
class LibraryApp:
    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library Management System")
        
        self.main_menu()
    
    def main_menu(self):
        tk.Label(self.root, text="Library Management System", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Add Book", command=self.add_book).pack(pady=5)
        tk.Button(self.root, text="Register Member", command=self.register_member).pack(pady=5)
        tk.Button(self.root, text="Borrow Book", command=self.borrow_book).pack(pady=5)
        tk.Button(self.root, text="Return Book", command=self.return_book).pack(pady=5)
        tk.Button(self.root, text="View Available Books", command=self.view_available_books).pack(pady=5)
        tk.Button(self.root, text="View Members", command=self.view_members).pack(pady=5)
    
    def add_book(self):
        self.popup_window("Add Book", self.add_book_callback, ["Book ID:", "Title:", "Author:"])
    
    def add_book_callback(self, book_id, title, author):
        book = Book(book_id, title, author)
        self.library.add_book(book)
        messagebox.showinfo("Success", "Book added successfully")
    
    def register_member(self):
        self.popup_window("Register Member", self.register_member_callback, ["Member ID:", "Name:"])
    
    def register_member_callback(self, member_id, name):
        member = Member(member_id, name)
        self.library.register_member(member)
        messagebox.showinfo("Success", "Member registered successfully")
    
    def borrow_book(self):
        available_books = self.library.view_available_books()
    
        if not available_books:
            messagebox.showinfo("Borrow Book", "No Books Available")
            return
    
        book_list = "\n".join([f"{b.book_id}: {b.title} by {b.author}" for b in available_books])
        messagebox.showinfo("Available Books", book_list)
        self.popup_window("Borrow Book", self.borrow_book_callback, ["Member ID:", "Book ID:"])

    def borrow_book_callback(self, member_id, book_id):
        book_title = self.library.borrow_book(member_id, book_id)
        member = next((m for m in self.library.members if m.member_id == member_id), None)
    
        if book_title and member:
            messagebox.showinfo("Success", f"{member.name} has borrowed {book_title}")
        else:
            messagebox.showerror("Error", "Book not available or invalid member ID")

    def return_book(self):
        if not self.library.borrowed_books:
            messagebox.showinfo("Return Book", "No Books Borrowed")
            return
    
        self.popup_window("Return Book", self.return_book_callback, ["Member ID:", "Book ID:"])
    
    def return_book_callback(self, member_id, book_id):
        if self.library.return_book(member_id, book_id):
            messagebox.showinfo("Success", "Book returned successfully")
        else:
            messagebox.showerror("Error", "Invalid return request")
    
    def view_available_books(self):
        books = self.library.view_available_books()
        book_list = "\n".join([f"{b.book_id}: {b.title} by {b.author}" for b in books])
        messagebox.showinfo("Available Books", book_list if book_list else "No books available")
    
    def view_members(self):
        members = self.library.view_members()
        member_list = "\n".join([f"{m.member_id}: {m.name} - Borrowed Books: {[b.title for b in m.borrowed_books]}" for m in members])
        messagebox.showinfo("Registered Members", member_list if member_list else "No members registered")
    
    def popup_window(self, title, callback, fields=[]):
        popup = tk.Toplevel(self.root)
        popup.title(title)

        entries = []
        for field in fields:
            tk.Label(popup, text=field).pack()
            entry = tk.Entry(popup)
            entry.pack()
            entries.append(entry)

        def submit():
            values = [entry.get() for entry in entries]
            callback(*values)
            popup.destroy()

        tk.Button(popup, text="Submit", command=submit).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
