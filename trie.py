import tkinter as tk
from tkinter import messagebox

# Backend: Trie with deletion
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def delete(self, word):
        def _delete(node, word, depth):
            if not node:
                return False

            if depth == len(word):
                if node.is_end_of_word:
                    node.is_end_of_word = False
                return len(node.children) == 0

            char = word[depth]
            if char in node.children:
                should_delete_child = _delete(node.children[char], word, depth + 1)
                if should_delete_child:
                    del node.children[char]
                    return not node.is_end_of_word and len(node.children) == 0

            return False

        _delete(self.root, word, 0)

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_words(node, prefix)

    def _collect_words(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)

        for char, child_node in node.children.items():
            words.extend(self._collect_words(child_node, prefix + char))
        return words


class AutocompleteApp:
    def __init__(self, root, trie):
        self.trie = trie
        self.root = root
        self.root.title("Autocomplete System")

        # Input label and field
        self.input_label = tk.Label(root, text="Enter Word/Prefix:")
        self.input_label.pack()
        self.input_field = tk.Entry(root, width=30)
        self.input_field.pack()
        self.input_field.bind("<KeyRelease>", self.update_suggestions)

        # Suggestions display
        self.suggestions_label = tk.Label(root, text="Suggestions:")
        self.suggestions_label.pack()
        self.suggestions_listbox = tk.Listbox(root, width=30, height=10)
        self.suggestions_listbox.pack()

        # Buttons to add or delete words
        self.add_word_button = tk.Button(root, text="Add Word", command=self.add_word)
        self.add_word_button.pack()
        self.delete_word_button = tk.Button(root, text="Delete Word", command=self.delete_word)
        self.delete_word_button.pack()

    def update_suggestions(self, event=None):
        # Fetch and display suggestions based on entered prefix
        prefix = self.input_field.get()
        suggestions = self.trie.starts_with(prefix)
        self.suggestions_listbox.delete(0, tk.END)  # Clear previous suggestions
        if suggestions:
            for word in suggestions:
                self.suggestions_listbox.insert(tk.END, word)
        else:
            self.suggestions_listbox.insert(tk.END, "No suggestions found")

    def add_word(self):
        word = self.input_field.get()
        if word:
            self.trie.insert(word)
            messagebox.showinfo("Success", f'Word "{word}" added to the Trie!')
            self.input_field.delete(0, tk.END)  # Clear the input field
            self.update_suggestions()
        else:
            messagebox.showwarning("Input Error", "Please enter a word to add.")

    def delete_word(self):
        word = self.input_field.get()
        if word:
            self.trie.delete(word)
            messagebox.showinfo("Success", f'Word "{word}" deleted from the Trie!')
            self.input_field.delete(0, tk.END)  # Clear the input field
            self.update_suggestions()
        else:
            messagebox.showwarning("Input Error", "Please enter a word to delete.")


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    trie = Trie()

    # Insert default words into Trie
    default_words = ["apple", "app", "ape", "bat", "ball", "cat", "car"]
    for word in default_words:
        trie.insert(word)

    app = AutocompleteApp(root, trie)
    root.mainloop()

