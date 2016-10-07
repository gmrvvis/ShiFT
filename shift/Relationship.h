/*
 * Copyright (c) 2014-2016 GMRV/URJC/UPM.
 *
 * Authors: Pablo Toharia <pablo.toharia@upm.es>
 *
 * This file is part of ShiFT
 *
 * This library is free software; you can redistribute it and/or modify it under
 * the terms of the GNU Lesser General Public License version 3.0 as published
 * by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 * details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 */
#ifndef __SHIFT__RELATIONSHIP__
#define __SHIFT__RELATIONSHIP__

#include "Entity.h"
#include <shift/api.h>
#include <unordered_set>
#include <unordered_map>

namespace shift
{

  class RelationshipOneToOne;
  class RelationshipOneToN;
  class RelationshipNToN;

  class Relationship
  {
  public:
    typedef enum
    {
      UNDEFINED,
      ONE_TO_ONE,
      ONE_TO_N,
      N_TO_N
    } TCardinality;

    SHIFT_API Relationship( void );
    SHIFT_API virtual ~Relationship( void ) {}
    SHIFT_API TCardinality cardinality( void ) const;
    SHIFT_API virtual RelationshipOneToOne* asOneToOne( void );
    SHIFT_API virtual RelationshipOneToN* asOneToN( void );
    SHIFT_API virtual RelationshipNToN* asNToN( void );

  protected:
    TCardinality _cardinality;

  };

  class RelationshipOneToOne
    : public Relationship
    , public std::unordered_map< unsigned int, unsigned int >
  {
  public:
    SHIFT_API RelationshipOneToOne( void );
    SHIFT_API virtual RelationshipOneToOne* asOneToOne( void );
  };

  class RelationshipOneToN
    : public Relationship
    , public std::unordered_map< unsigned int,
                                 std::unordered_set< unsigned int >>
  {
  public:
    SHIFT_API RelationshipOneToN( void );
    SHIFT_API virtual RelationshipOneToN* asOneToN( void );
  };

    class RelationshipNToN
    : public Relationship
    , public std::vector< std::tuple< std::unordered_set< unsigned int >,
                                      std::unordered_set< unsigned int >>>
  {
  public:
    SHIFT_API RelationshipNToN( void );
    SHIFT_API virtual RelationshipNToN* asNToN( void );
  };

} // namespace shift
#endif // __SHIFT__RELATIONSHIP__