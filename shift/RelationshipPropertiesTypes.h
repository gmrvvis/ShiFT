/*
 * Copyright (c) 2014-2016 GMRV/URJC/UPM.
 *
 * Authors: Juan Jose Garcia Cantero <juanjose.garcia@urjc.es>
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
#ifndef __SHIFT_RELATIONSHIP_PROPERTIES_TYPES__
#define __SHIFT_RELATIONSHIP_PROPERTIES_TYPES__

#include "Relationship.h"
#include <shift/api.h>
#include <vector>
#include <string>
#include <unordered_map>

namespace shift
{
  class RelationshipPropertiesTypes
  {
  public:

    typedef std::unordered_map< std::string, RelationshipProperties* >
      TRelationshipPropertiesTypes;

    virtual ~RelationshipPropertiesTypes( void ){ }

    const TRelationshipPropertiesTypes& relationshipPropertiesTypes( void )
      const { return _relationshipPropertiesTypes; }

    RelationshipProperties* getRelationshipProperties(
      const std::string relationshipName_ )
    {
      auto relPropIt = _relationshipPropertiesTypes.find( relationshipName_ );
      if ( relPropIt != _relationshipPropertiesTypes.end( ))
        return relPropIt->second;
      else
        return nullptr;
    }

  protected:
    TRelationshipPropertiesTypes _relationshipPropertiesTypes;

  };

}

#endif
