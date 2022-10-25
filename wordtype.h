/*********************************************************************
 *
 *  wordtype.h
 *
 *  Interface for Word datatype used in phrase structure rules
 *
 ********************************************************************/

#ifndef WORDTYPE_H
#define WORDTYPE_H

#include <string>

class Word
{
public:
  Word(const std::string s);
  inline std::string getWord() { return s; }
  virtual std::string getTypeID() = 0;
  
private:
  std::string s;
};

class FeatureWord : public Word
{
public:
  FeatureWord(const std::string s);
  FeatureWord(const std::string s, const std::string f);
  inline std::string getFeatures() { return f; }
  virtual void setFeatures(const std::string f) = 0;
  
private:
  std::string f;
};

class A : public Word
{
public:
  A(const std::string s);
  inline std::string getTypeID() { return "A"; }
};

class Adv : public Word
{
public:
  Adv(const std::string s);
  inline std::string getTypeID() { return "Adv"; }
};

class C : public FeatureWord
{
public:
  C(const std::string s);
  C(const std::string s, const std::string f);
  void setFeatures(const std::string f);
  inline std::string getTypeID() { return "C"; }
};

class D : public FeatureWord
{
public:
  D(const std::string s);
  D(const std::string s, const std::string f);
  void setFeatures(const std::string f);
  inline std::string getTypeID() { return "D"; }
};

class N : public Word
{
public:
  N(const std::string s);
  inline std::string getTypeID() { return "N"; }
};

class Neg : public Word
{
public:
  Neg(const std::string s);
  inline std::string getTypeID() { return "Neg"; }
};

class P : public Word
{
public:
  P(const std::string s);
  inline std::string getTypeID() { return "P"; }
};

class T : public FeatureWord
{
public:
  T(const std::string s);
  T(const std::string s, const std::string f);
  void setFeatures(const std::string f);
  inline std::string getTypeID() { return "T"; }
};

class V : public Word
{
public:
  V(const std::string s);
  inline std::string getTypeID() { return "V"; }
};

#endif
