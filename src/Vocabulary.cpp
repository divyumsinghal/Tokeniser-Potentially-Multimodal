#include "Vocabulary.hpp"
#include "Utils.hpp"

std::string Vocabulary::getTokenFromID(int id) const
{
    if (id >= 0 && id < id_to_token.size())
    {
        return id_to_token[id];
    }

    return utils::invalid_token;
}