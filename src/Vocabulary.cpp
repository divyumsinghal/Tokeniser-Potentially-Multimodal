#include "Vocabulary.hpp"

#include <limits>
#include <numeric>

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

/// @brief Save the Vocabulary to a file.
/// Save it as a YAML, storing the id, token and frequency.
/// @param path The file path to save the vocabulary.
void Vocabulary::save(const std::string &path = "data/vocabulary.yaml") {
  // TODO: Check, maybe Improve

  std::ofstream file(path);
  if (!file.is_open()) {
    throw std::runtime_error(
        "[Vocabulary.cpp] [Vocabulary::save] Failed to open file: " + path);
  }

  file << "id_to_token:\n";
  for (size_t i = 0; i < id_to_token.size(); ++i) {
    file << i << " :\n"
         << "   \"" << id_to_token[i]
         << "\" : " << token_frequency[id_to_token[i]] << "\n";
  }

  file.close();
}

/// @brief Load the Vocabulary from a file.
/// Load it from a YAML file, parsing the id, token and frequency.
/// Basically Undoes what save() does.
/// @param path The file path to load the vocabulary from.
void Vocabulary::load(const std::string &path = "data/vocabulary.yaml") {
  // TODO: CHeck, maybe Improve

  std::ifstream file(path);
  if (!file.is_open()) {
    throw std::runtime_error(
        "[Vocabulary.cpp] [Vocabulary::load] Failed to open file: " + path);
  }

  if (!id_to_token.empty() || !token_to_id.empty() ||
      !token_frequency.empty()) {
    throw std::runtime_error(
        "[Vocabulary.cpp] [Vocabulary::load] Vocabulary is already loaded, "
        "clear it before loading again.");
  }

  std::string line;
  while (std::getline(file, line)) {
    if (line.empty()) continue;  // Skip empty lines

    size_t colonPos = line.find(':');
    if (colonPos == std::string::npos) continue;  // Invalid line format

    std::string token = line.substr(0, colonPos);
    std::string frequencyStr = line.substr(colonPos + 1);
    int frequency = std::stoi(frequencyStr);

    int id = addToken(token);
    token_frequency[token] = frequency;
  }
  file.close();
  std::cout << "[Vocabulary.cpp] [Vocabulary::load] Loaded "
            << id_to_token.size() << " tokens from " << path << std::endl;
  if (id_to_token.empty()) {
    throw std::runtime_error(
        "[Vocabulary.cpp] [Vocabulary::load] No tokens found in the file: " +
        path);
  }
  // Sanity check
  for (const auto &pair : token_to_id) {
    if (pair.second < 0 || pair.second >= id_to_token.size()) {
      throw std::runtime_error(
          "[Vocabulary.cpp] [Vocabulary::load] Invalid token ID: " +
          std::to_string(pair.second) + " for token: " + pair.first);
    }
  }
  for (size_t i = 0; i < id_to_token.size(); ++i) {
    if (token_to_id.find(id_to_token[i]) == token_to_id.end()) {
      throw std::runtime_error(
          "[Vocabulary.cpp] [Vocabulary::load] Token not found in "
          "token_to_id: " +
          id_to_token[i]);
    }
  }

  // Print Stats
  std::cout << "[Vocabulary.cpp] [Vocabulary::load] Vocabulary loaded "
               "successfully from "
            << path << std::endl;
  std::cout << "[Vocabulary.cpp] [Vocabulary::load] Vocabulary size: "
            << id_to_token.size() << std::endl;
  std::cout << "[Vocabulary.cpp] [Vocabulary::load] Unique tokens: "
            << token_to_id.size() << std::endl;
  std::cout << "[Vocabulary.cpp] [Vocabulary::load] Total frequency: "
            << std::accumulate(
                   token_frequency.begin(), token_frequency.end(), 0,
                   [](int sum, const auto &pair) { return sum + pair.second; })
            << std::endl;
  std::cout << "[Vocabulary.cpp] [Vocabulary::load] Unique frequencies: "
            << token_frequency.size() << std::endl;
  std::cout << "[Vocabulary.cpp] [Vocabulary::load] First token: "
            << (id_to_token.empty() ? "None" : id_to_token[0]) << std::endl;
  std::cout << "[Vocabulary.cpp] [Vocabulary::load] Last token: "
            << (id_to_token.empty() ? "None" : id_to_token.back()) << std::endl;
}
