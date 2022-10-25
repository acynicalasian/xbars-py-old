/*********************************************************************
 *
 *  wordtype.cpp
 *
 *  Implementation of wordtype.h
 *
 ********************************************************************/

#include <iostream>
#include <string>
#include "wordtype.h"

Word :: Word(const std::string s) : s(s) {}

FeatureWord :: FeatureWord(const std::string s) : s(s), f("") {}
FeatureWord :: FeatureWord(const std::string s, const std::string f) : s(s)
{ FeatureWord::setFeatures(f); }

A :: A(const std::string s) : Word(s) {}

Adv :: Adv(const std::string s) : Word(s) {}

C :: C(const std::string s) : FeatureWord(s) {}
C :: C(const std::string s, const std::string f) : FeatureWord(s, f) {}
C :: void setFeatures(const std::string f)
{
  try
  {
    switch (f)
    {
    case "[+Q]":
    case "[+Q][+wh]":
    case "[+wh]":
    case "":
      this->f = f;
      break;
    default:
      throw (f);
    }
  }
  catch (const std::string s)
    std::cerr << "Invalid feature string for complementizer: " << s <<
      std::endl;
}

D :: D(const std::string s) : FeatureWord(s) {}
D :: D(const std::string s, const std::string f) : FeatureWord(s, f) {}
D :: void setFeatures(const std::string f)
{
  try
  {
    if (f == "[+wh]")
      this->f = f;
    else
      throw (f);
  }
  catch (const std::string s)
    std::cerr << "Invalid feature string for determiner: " << s <<
      std::endl;
}

N :: N(const std::string s) : Word(s) {}

Neg :: Neg(const std::string s) : Word(s) {}

P :: P(const std::string s) : Word(s) {}

T :: T(const std::string s) : FeatureWord(s) {}
T :: T(const std::string s, const std::string f) : FeatureWord(s, f) {}
T :: void setFeatures(const std::string f)
{
  try
  {
    switch (f)
    {
    case "[-tense]":
    case "[+past]":
    case "[+future]":
      this->f = f;
      break;
    default:
      throw (f);
    }
  }
  catch (const std::string s)
    std::cerr << "Invalid feature string for tense word: " << s <<
      std::endl;
}

V :: V(const std::string s) : Word(s) {}
