# Distance Vector project for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, Jeffrey Randow, new VM fixes by Jared Scott and James Lohse.

from Node import *
from helpers import *


class DistanceVector(Node):

    def __init__(self, name, topolink, outgoing_links, incoming_links):
        """ Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here."""

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)

        # TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data

        # should keep track of the NODES that are linked to this node
        # the WEIGHTS of the path (min -50, max 50). -99 is equivalent of negative infinity
        # need to have some way to determine if there is an infinite negative cycle traversal

        # Data Structure to track distance vectors
        # array of objects. nodeName: string, value: number
        #
        # Condition for 99 - publish messages. If the distance is -99, stop publishing

        # we only want to send messages to incoming links/UPSTREAM neighbours only. E.g. AA --> AD. But doesn't care about AB --> AA

        self.distance_vector_table = {
            self.name: 0
        }


    def send_initial_messages(self):
        """ This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here.

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight """

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py

        # print('This is incoming links: ', self.name, self.incoming_links[0].name)
        # Incoming Links[0] is AB. This means that AB --> AA
        # Since we want to publish to AD, we should be sending out to our outgoing links

        # Message format -> (origin node, origin node distance vector)
        # we only want to send out to the UPSTREAM neighbours
        # e.g. AA --> AD. So AA will send a message to AD

        for outgoing_link in self.outgoing_links:
            ## I THINK MESSAGE needs to have ORIGIN, DESTINATION, DISTANCE
            ## It can't just be ORIGIN, DISTANCE (i.e. it must be 3, not 2)
            # Message = (sending_node, destination_name, distance)
            message = (self.name, outgoing_link.name, 0)
            self.messages.append(message)
        # print('This is after: ', self.name, self.messages)


    def process_BF(self):
        """ This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. """

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages
        #
        BREAK_LIMIT = -99

        updated = False
        for msg in self.messages:
            # get neighbour weight
            sending_node, destination, published_distance = msg

            if destination == self.name:
                continue
            if published_distance == BREAK_LIMIT and self.distance_vector_table[destination] != BREAK_LIMIT:
                self.distance_vector_table[destination] = BREAK_LIMIT
                updated = True
                continue

            if self.distance_vector_table.get(destination, "") == "":

                result = self.get_outgoing_neighbor_weight(destination)
                if result == "Node Not Found":
                    # (A)
                    # if not a neighbour, we need to add it
                    distance_to_sending_node = self.distance_vector_table[sending_node]
                    self.distance_vector_table[destination] = distance_to_sending_node + published_distance
                    updated = True
                    # print(f'(A) Updated: {self.name,destination}: {self.distance_vector_table}')
                elif result != "Node Not Found":
                    # (B)
                    name, neighbour_weight = result
                    self.distance_vector_table[destination] = int(neighbour_weight)
                    updated = True
                    # print(f'(B) Updated: {self.name,destination}: {self.distance_vector_table}')
            else:
                # perform the comparison

                current_cost = self.distance_vector_table.get(destination, "")

                result = self.get_outgoing_neighbor_weight(sending_node)
                if result == "Node Not Found":
                    raise Exception(f"Node not found. self.name: {self.name}, outgoing_link: {destination}")
                else:
                    name, neighbour_weight = self.get_outgoing_neighbor_weight(sending_node)
                    comparison_cost = published_distance + neighbour_weight
                    print('Self.Name, Sending Node, destination, neighbour_weight, published_distance', [self.name, sending_node, destination, neighbour_weight, published_distance])
                    if comparison_cost < current_cost and current_cost != BREAK_LIMIT:
                        # (C)
                        if comparison_cost < BREAK_LIMIT:
                            self.distance_vector_table[destination] = BREAK_LIMIT
                            print(f'(C) Updated: {self.name,destination}: {self.distance_vector_table}')
                            updated = True
                        else:
                            # (D)
                            self.distance_vector_table[destination] = comparison_cost
                            print(f'(D) Updated: {self.name,destination}: {self.distance_vector_table}')
                            updated = True


        # Empty queue
        self.messages = []

        # print("This is updated distance vector table: ", self.distance_vector_table)
        # print('This is updated_distance: ', updated_distances)
        if updated == True:
            self.publish_message(self.incoming_links, self.distance_vector_table)

    def publish_message(self, incoming_links, distance_vector_table):
        # incoming_link_names = [link.name for link in incoming_links]
        # print(f"I am node: {self.name}, I am updating my links: {incoming_link_names}")
        for incoming_link in incoming_links:
            # tell the incoming links that there is a shorter distance
            for key, value in distance_vector_table.items():
                message = (self.name, key, value)
                # print('This is the message i am sending: ', message)
                self.send_msg(message, incoming_link.name)


    def log_distances(self):
        """ This function is called immedately after process_BF each round.  It
        prints distances to the console and the log file in the following format (no whitespace either end):

        A:(A,0) (B,1) (C,-2)

        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 """

        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.
        # add_entry("A", "(A,0) (B,1) (C,-2)")

        vectors = []

        for key, value in self.distance_vector_table.items():
            vector = f"({key},{value})"
            vectors.append(vector)
        string = " ".join(vectors)
        add_entry(self.name, string)
