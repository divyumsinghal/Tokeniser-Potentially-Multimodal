#pragma once
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

/// @brief A simple vocabulary class for managing tokens and their IDs.
/// A Token is a string that can be mapped to an integer ID.
class Vocabulary {
 private:
  std::unordered_map<std::string, int> token_to_id;  // Get Token ID from string
  std::vector<std::string>
      id_to_token;  // Reverse Lookup - Get string from Token ID
  std::unordered_map<std::string, int>
      token_frequency;  // For tracking token frequency

 public:
  int addToken(const std::string &token);
  int getTokenID(const std::string &token) const;
  std::string getTokenFromID(int id) const;
  void save(const std::string &path);
  void load(const std::string &path);
};
