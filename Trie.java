public class Trie {
    private TrieNode root;

    public Trie() {
        root = new TrieNode();
    }

    private static class TrieNode {
        TrieNode[] children;
        boolean isEndOfWord;

        public TrieNode() {
            children = new TrieNode[26];
            isEndOfWord = false;
        }
    }

    public void insert(String word) {
        TrieNode current = root;
        for (char ch : word.toCharArray()) {
            int index = ch - 'a';
            if (current.children[index] == null) {
                current.children[index] = new TrieNode();
            }
            current = current.children[index];
        }
        current.isEndOfWord = true;
    }

    public boolean search(String word) {
        TrieNode current = root;
        for (char ch : word.toCharArray()) {
            int index = ch - 'a';
            if (current.children[index] == null) {
                return false;
            }
            current = current.children[index];
        }
        return current.isEndOfWord;
    }

    public boolean startsWith(String prefix) {
        TrieNode current = root;
        for (char ch : prefix.toCharArray()) {
            int index = ch - 'a';
            if (current.children[index] == null) {
                return false;
            }
            current = current.children[index];
        }
        return true;
    }

    public void delete(String word) {
        deleteHelper(root, word, 0);
    }

    private boolean deleteHelper(TrieNode current, String word, int index) {
        if (index == word.length()) {
            if (!current.isEndOfWord) {
                return false;
            }
            current.isEndOfWord = false;
            return current.children.length == 0;
        }

        int charIndex = word.charAt(index) - 'a';
        boolean childDeleted = deleteHelper(current.children[charIndex], word, index + 1);

        if (childDeleted) {
            current.children[charIndex] = null;
            return current.children.length == 0 && !current.isEndOfWord;
        }

        return false;
    }

    public static void main(String[] args) {
        Trie trie = new Trie();

        trie.insert("apple");
        trie.insert("apps");
        trie.insert("ape");

        System.out.println(trie.search("apple")); // Output: true
        System.out.println(trie.search("app"));  // Output: false
        System.out.println(trie.startsWith("ap")); // Output: true

        trie.delete("apple");
        System.out.println(trie.search("apple")); // Output: false

        // Additional test cases:
        trie.insert("banana");
        trie.insert("band");
        trie.insert("bandana");

        System.out.println(trie.startsWith("ban")); // Output: true
        System.out.println(trie.search("bandana")); // Output: true
        System.out.println(trie.search("bandage")); // Output: false

        trie.delete("band");
        System.out.println(trie.search("band")); // Output: false
        System.out.println(trie.search("bandana")); // Output: true
    }
}
