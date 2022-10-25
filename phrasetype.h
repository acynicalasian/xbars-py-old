/*********************************************************************
 *
 *  phrasetype.h
 *
 *  Interface for Phrase datatype used in phrase structure rules
 *
 ********************************************************************/

#ifndef PHRASETYPE_H
#define PHRASETYPE_H

#include <string>
#include <vector>
#include "wordtype.h"

class Phrase : private Word
{
public:
  Phrase(Word* c);
  Phrase(Word* c1, Word* c2);
  Phrase(Word* c1, Word* c2, Word* c3);
  inline std::vector<Word*> getChildren() { return c; }
  void addChild(Word* w);

private:
  std::vector<Word*> c;
};

class AP : public Phrase
{
public:
  // TO-DO

  inline std::string getTypeID() { return "AP"; }
};
  
class AdvP : public Phrase
{
public:
  // TO-DO

  inline std::string getTypeID() { return "AdvP"; }
};

class CP : public Phrase
{
public:
  // TO-DO

  inline std::string getTypeID() { return "CP"; }
};

class DP : public Phrase
{
public:
  // TO-DO

  inline std::string getTypeID() { return "DP"; }
};

class NP : public Phrase
{
public:
  // TO-DO

  inline std::string getTypeID() { return "NP"; }
};

class NegP : public Phrase
{
public:
  // TO-DO

  inline std::string getTypeID() { return "NegP"; }
};

class PP : public Phrase
{
public:
  // TO-DO

  inline std::string getTypeID() { return "PP"; }
};

class TP : public Phrase
{
public:
  // TO-DO

  inline std::string getTypeID() { return "TP"; }
};

class VP : public Phrase
{
public:
  // TO-DO

  inline std::string getTypeID() { return "VP"; }
};

class BoundT : public Phrase
{
public:
  BoundT(V* v, T* t);
  // TO-DO

  inline std::string getTypeID() { return "T"; }
};

#endif
