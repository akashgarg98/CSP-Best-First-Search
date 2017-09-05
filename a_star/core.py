import time

from a_star.agenda import Agenda
from a_star.node import Node

class AStarCore():

    agenda = None
    closed = {}

    # Stats:
    nodes_generated = 0

    def __init__(self, agenda: Agenda):
        self.start_time = time.time()
        self.end_time = 0
        self.agenda = agenda

    def is_solution(self, node):
        """
        This needs to be overwritten by specified algorithm. The method should check
        if a node is a solution to the problem A* is trying to solve.
        """
        pass

    def total_nodes(self) -> int:
        return len(self.closed)

    def time_used(self) -> float:
        return self.end_time-self.start_time

    def best_first_search(self):
        """
        Finds a solution using best-first search.

        Prerequisite: The node used needs to be a specialized node for the problem
        to be solved.
        """
        while not self.agenda.is_empty():
            # Getting next node from the agenda:
            node = self.agenda.dequeue() # type: Node

            self.closed[hash(node)] = node
            # print(node.board)
            # If the node is a solution, return it:

            if node.is_solution():
                self.end_time = time.time()
                return node

            node.create_children()
            # Finding all children and looping through.
            for child in node.children:

                # Checking if the child has been created before:
                if hash(child) in self.closed:
                    # What happens when a child has been seen before? Compare the
                    # child's previous steps to the steps used by the previously seen
                    # node.
                    other_node = self.closed[hash(child)]
                    if child >= other_node:
                        continue
                    else: # child < other_node
                        # Calculate new values for all children of other_node.
                        other_node.recalculate_G_for_all_children(child)

                elif child in self.agenda:
                    # Node has been seen before, but has not yet been evaluated.
                    # It should not have any children if the elif is True.
                    other_node = self.agenda.get_node(hash(child))
                    if child >= other_node:
                        # If the same solution is found, but the existing solution
                        # is better. Do nothing.
                        continue
                    else:
                        # self.agenda.remove_node(other_node) # no need to remove. Correct answer will be eval first
                        self.agenda.enqueue(child)
                else:
                    # Node has not been seen or evaluated before. Add to agenda.
                    self.agenda.enqueue(child) # NOTE! Slow.
