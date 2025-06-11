#include "Vocabulary.hpp"

#include <limits>

#include "Utils.hpp"

/// @brief Adds a token to the vocabulary and returns its ID.
/// If the token already exists, it returns the existing ID.
/// @param token The token to add.
/// @return The ID of the token.
int Vocabulary::addToken(const std::string &token) {
  if (token.empty()) {
    throw std::invalid_argument(
        "[Vocabulary.cpp] [Vocabulary::addToken] Token cannot be empty");
  }

  if (token_to_id.find(token) == token_to_id.end()) {
    int id = id_to_token.size();  // New Token, assign next available ID

    if (id >= std::numeric_limits<int>::max()) {
      throw std::runtime_error(
          "[Vocabulary.cpp] [Vocabulary::addToken] Vocabulary size limit "
          "reached");
    }

    token_to_id[token] = id;
    id_to_token.push_back(token);
    token_frequency[token] = 1;  // Initialize frequency to 1 for new token
    return id;
  }

  token_frequency[token]++;
  int id = token_to_id[token];

  if (id_to_token[id] != token)  // Run a Sanity check
  {
    throw std::runtime_error(
        "[Vocabulary.cpp] [Vocabulary::addToken] ID mismatch for token: " +
        token);
  }

  return id;
}

/// @brief Get the ID of a token.
/// @param token The token string.
/// @return The ID of the token, or an invalid token ID if not found.
int Vocabulary::getTokenID(const std::string &token) const {
  auto it = token_to_id.find(token);
  if (it != token_to_id.end()) {
    // Run a Sanity check
    if (it->second < 0 || it->second >= id_to_token.size()) {
      throw std::runtime_error(
          "[Vocabulary.cpp] [Vocabulary::getTokenID] Invalid token ID: " +
          std::to_string(it->second));
    }

    // Or 2
    if (id_to_token[it->second] != token)  // Run a Sanity check
    {
      throw std::runtime_error(
          "[Vocabulary.cpp] [Vocabulary::getTokenID] ID mismatch for token: " +
          token);
    }

    return it->second;
  }
  return utils::invalid_token_id;  // Invalid token ID
}

/// @brief Get the token string from its ID.
/// @param id The ID of the token.
/// @return The token string, or an invalid token string if not found.
std::string Vocabulary::getTokenFromID(int id) const {
  if (id >= 0 && id < id_to_token.size()) {
    return id_to_token[id];
  }

  return utils::invalid_token;
}