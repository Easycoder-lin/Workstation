#include "board/board.hpp"
#include "math_lib/maths.hpp"
#include <stdio.h>
#include <random>
#include <vector>
#include <memory>
#include <cmath>

#define SIMULATION_BATCH_NUM 100
#define MAX_SIMULATION_COUNT 10000

// MCTS Node Structure
struct MCTSNode {
    Board state;
    std::vector<std::unique_ptr<MCTSNode>> children;
    MCTSNode* parent;
    unsigned int visits;
    unsigned int wins;
    int move_index;

    MCTSNode(Board state, MCTSNode* parent = nullptr, int move_index = -1)
        : state(state), parent(parent), visits(0), wins(0), move_index(move_index) {}

    bool is_fully_expanded() const {
        return children.size() == static_cast<size_t>(state.move_count);
    }
};

float ucb_value(unsigned int total_simulations, unsigned int node_wins, unsigned int node_visits, float exploration = 1.41421f) {
    if (node_visits == 0) {
        return std::numeric_limits<float>::max();
    }
    return static_cast<float>(node_wins) / static_cast<float>(node_visits) +
           exploration * sqrt(log(static_cast<float>(total_simulations)) / static_cast<float>(node_visits));
}

MCTSNode* select_best_ucb_node(MCTSNode* node, float exploration) {
    MCTSNode* best_node = nullptr;
    float best_ucb = -1;
    for (auto& child : node->children) {
        float ucb = ucb_value(node->visits, child->wins, child->visits, exploration);
        if (ucb > best_ucb) {
            best_ucb = ucb;
            best_node = child.get();
        }
    }
    return best_node;
}

void expand_node(MCTSNode* node) {
    if (!node->is_fully_expanded()) {
        Board new_state = node->state;
        new_state.move(node->children.size());
        node->children.push_back(std::make_unique<MCTSNode>(new_state, node, node->children.size()));
    }
}

bool simulate(Board& board) {
    static std::mt19937 random_num(std::random_device{}());
    Board board_copy = board;
    int depth = 0;
    while (!board_copy.check_winner() && depth < 50) { // Limit simulation depth to avoid long runs
        board_copy.generate_moves();
        board_copy.move(random_num() % board_copy.move_count);
        depth++;
    }
    return board_copy.moving_color == board.moving_color;
}

void backpropagate(MCTSNode* node, bool win) {
    while (node != nullptr) {
        node->visits++;
        if (win) {
            node->wins++;
        }
        node = node->parent;
    }
}

int MCTS(Board root_state, unsigned int max_simulations, float exploration) {
    MCTSNode root(root_state);
    root.state.generate_moves();

    unsigned int total_simulations = 0;
    while (total_simulations < max_simulations) {
        // Selection
        MCTSNode* node = &root;
        while (node->is_fully_expanded() && !node->children.empty()) {
            node = select_best_ucb_node(node, exploration);
        }

        // Expansion
        if (!node->is_fully_expanded()) {
            expand_node(node);
            node = node->children.back().get();
        }

        // Simulation
        bool win = simulate(node->state);

        // Backpropagation
        backpropagate(node, win);

        total_simulations++;
    }

    // Return the best move
    MCTSNode* best_child = nullptr;
    float best_win_rate = -1;
    for (auto& child : root.children) {
        float win_rate = static_cast<float>(child->wins) / static_cast<float>(child->visits);
        if (win_rate > best_win_rate) {
            best_win_rate = win_rate;
            best_child = child.get();
        }
    }
    return best_child ? best_child->move_index : -1;
}

int Board::decide() {
    return MCTS(*this, MAX_SIMULATION_COUNT, 1.41421f);
}

int Board::first_move_decide_dice() {
    static std::mt19937 random_num(std::random_device{}());
    return random_num() % PIECE_NUM;  // Simple random decision for the first move dice value
}
