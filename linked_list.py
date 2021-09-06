class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail_last_node = None

    # convert the linked list into an array

    def to_list(self):
        list = []
        if self.head is None:
            return list

        node = self.head
        while node:
            list.append(node.data)
            node = node.next_node
        return list

    def print_ll_func(self):
        linked_list_storage = ""
        node = self.head
        if node is Node:
            print(None)
        while node:
            linked_list_storage += f"{str(node.data)} ->"
            node = node.next_node

        linked_list_storage += " None"
        print(linked_list_storage)

    def insert_beginning(self, data):
        if self.head is None:
            self.head = Node(data,None)
            self.tail_last_node = self.head

        new_node = Node(data, self.head)
        self.head = new_node

    def insert_at_end(self, data):
        if self.head is None:
            self.insert_beginning(data)
            return

        self.tail_last_node.next_node = Node(data, None)
        self.tail_last_node = self.tail_last_node.next_node

    def get_user_by_id(self, user_id):
        node = self.head
        while node:
            if node.data["id"] is int(user_id):
                return node.data

            node = node.next_node
        return None