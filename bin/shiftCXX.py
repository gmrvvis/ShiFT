#!/usr/bin/python3
import json
import sys

def print_header( objectType, reps, rep, file ):
    print( "shiftCXX: Generating " + file )
    header = ""
    includes = ""
    body = ""

    header_define = "__" + rep[ "namespace" ].upper( ).replace("::", "__") + \
                        "__" + rep[ "name" ].upper( ) + "__"
    header += "#ifndef " + header_define + "\n"
    header += "#define " + header_define

    includes += "\n\n#include <shift/shift.h>\n"
    includes += "\n"

    if "includes" in rep:
        customIncludes = rep[ "includes" ]
        for include in customIncludes :
            includes += "#include " + include + "\n"

    # Namespaces
    namespaces = rep[ "namespace" ].split( "::" )
    for namespace in namespaces :
        body += "namespace " + namespace + "\n"
        body += "{\n"

    # Class
    body += "  class " + rep[ "name" ] + "\n"
    if objectType == "Representation" :
        body += "    : public shift::Representation\n"
    else :
        if objectType == "Relationship" :
            body += "    : public shift::RelationshipProperties\n"
        else :
            if objectType == "Entity" :
                body += "    : public shift::Entity\n"
            else :
                raise Exception('objectType unknown')
    body += "  {\n"
    body += "  public:\n"

    # Types
    for type in rep[ "types" ] :

        if type[ "class" ] == "enum" :
            body += "    typedef enum\n"
            body += "    {\n"
            for value in type[ "values" ] :
                body += "       " + value + ",\n"
            body += "       " + type[ "name" ].upper( ) + "_UNDEFINED\n"
            body += "    } " + type[ "name" ] + ";\n\n"

        if type[ "class" ] == "vector" :
            includes += "#include <vector>\n"
            if type[ "element" ].replace("*", "") in reps :
                includes += "#include <shift_" +\
                type[ "element" ].replace("*", "") + ".h>\n"

            body += "    typedef std::vector< " + type[ "element" ] + \
                    " > " + type[ "name" ] + ";\n\n"

    # Constructor
    body += "    " + rep[ "name" ] + "( \n"
    i = 1
    for prop in rep[ "properties" ] :
        if prop[ "type" ] in reps :
            includes += "#include <shift_" + prop[ "type" ] + ".h>\n"

        body += "      " + prop[ "type" ] + " " + \
                prop[ "name" ].replace(" ", "") + " = " + \
                prop[ "type" ] + "( )"
        if i == len( rep[ "properties" ] ) :
            body += "\n    );\n"
        else :
            body += ",\n"
            i = i + 1

    # Copy constructor
    body += "    " + rep[ "name" ] + "( const " + rep[ "name" ] + "& );\n"
    # Destructor
    body += "    virtual ~" + rep[ "name" ] +  "( void );\n"

    # create method for entities
    if objectType == "Entity" :
        body += "    virtual shift::Entity* create( void ) const final;\n"

    if objectType == "Relationship" :
        body += "    virtual shift::RelationshipProperties* create( void ) const final;\n"
    
    # subentity method
    if objectType == "Entity" and "subentity" in rep[ "flags" ] :
        body += "    inline virtual bool isSubEntity( void ) final { return true; }\n"

    # propertyFlags method
    if objectType == "Entity" :
        body += "    inline virtual bool hasPropertyFlag( const std::string& propertyLabel,\n" + \
                "                                         shift::Entity::TPropertyFlag flag ) const final\n" +\
                "    {\n" + \
                "      return ( " + rep[ "name"] + "::_propertyFlags[ propertyLabel ].count( flag ) > 0 );\n" + \
                "    }\n\n"

        # propertyFlags static map
        body += "  protected:\n" + \
                "    static shift::Entity::TPropertiesFlagsMap _propertyFlags; \n"

    # end of class
    body += "  };\n"
    # body += "}\n"

    for namespace in namespaces :
        body += "}\n"

    body += "#endif // " + header_define + "\n"

    # print header
    # print includes
    # print body
    f = open( file, 'w')
    f.write( "// File generated by shiftCXX.py. Do not edit.\n" )
    f.write( header )
    f.write( includes )
    f.write( body )


def print_impl( objectType, rep, file ):
    print( "shiftCXX: Generating " + file )
    includes = ""
    body = ""

    includes += "#include <shift_" + rep[ "name" ] + ".h>\n"

    # Namespaces
    namespaces = rep[ "namespace" ].split( "::" )
    for namespace in namespaces :
        body += "namespace " + namespace + "\n"
        body += "{\n"

    # property flags map initialization
    if objectType == "Entity" :
        body += "  shift::Entity::TPropertiesFlagsMap " + rep[ "name" ] + "::_propertyFlags =\n" + \
                "  {\n"

        for prop in rep[ "properties" ] :
            body += "  { \"" + prop[ "name" ] + "\",\n    {\n"
            if "flags" in prop :
                for flag in prop[ "flags" ] :
                    body += "       shift::Entity::TPropertyFlag::" + flag;
                    if prop[ "flags"].index( flag ) != len( prop[ "flags"] ) - 1 :
                        body += ","
                    body += "\n"
            body += "    }\n"
            body += "  }"
            if rep[ "properties"].index( prop ) != len( rep[ "properties" ] ) - 1 :
                body += ","
            body += "\n"
        body += "  };\n\n"

    # Constructor
    body += "  " + rep[ "name" ] + "::" + rep[ "name" ] + "(\n"
    i = 1;
    for prop in rep[ "properties" ] :
        body += "      " + prop[ "type" ] + " " + \
                prop[ "name" ].replace(" ", "") + "__"
        if i == len( rep[ "properties" ] ) :
            body += " )\n"
        else :
            body += ",\n"
            i = i + 1
    body += "  {\n"

    types = rep[ "types" ]

    for prop in rep[ "properties" ] :

        type = {}
        for t in types :
            if t[ "name" ] == prop[ "type" ] :
                type = t
                break;
        enumValues = ""
        if type != {} and type[ "name" ] == prop[ "type" ] and  type[ "class" ] == "enum" :
            enumValues = ",\n      {"
            values = type[ "values" ]
            for value in values :
                enumValues += "\n        { " + value + ", \"" + value + "\" }"
                if values.index( value ) != len( values ) - 1 :
                    enumValues += ", "
            enumValues += "\n      }"

        body += "    fires::PropertyManager::registerProperty<" +\
                prop[ "type" ] +\
                ">( this, \"" +\
                prop[ "name" ] + "\", " \
                + prop[ "name" ].replace(" ", "") + "__" + enumValues + " );\n"
    body += "  }\n"
    # Copy constructor
    body += "  " + rep[ "name" ] + "::" + rep[ "name" ] + \
            "( const " + rep[ "name" ] + "& other )\n  {"
    body += "\n"
    for prop in rep[ "properties" ] :
        body += "    this->registerProperty(\n      \"" + prop[ "name" ] \
                + "\",\n" + "       other.getProperty( \"" + prop[ "name" ] \
                + "\" ).value< " +  prop[ "type" ] + " >( ));\n"
    body += "  }\n"
    body += "  " + rep[ "name" ] + "::~" + rep[ "name" ] +  "( void ) {}\n"

    # create method
    if objectType == "Entity" :
        body += "  shift::Entity* " + rep[ "name" ] + "::create( void ) const \n"
        body += "  {\n"
        body += "    return new " + rep[ "name" ] + "( *this );\n"
        body += "  }\n"

    if objectType == "Relationship" :
        body += "  shift::RelationshipProperties* " + rep[ "name" ] + "::create( void ) const \n"
        body += "  {\n"
        body += "    return new " + rep[ "name" ] + "( *this );\n"
        body += "  }\n"

    for namespace in namespaces :
        body += "}\n"

    f = open( file, 'w')

    f.write( "// File generated by shiftCXX.py. Do not edit.\n" )
    f.write( includes )
    f.write( body )

def generateDomain( name ) :
    return ""

def main( argv ) :

    objectType = argv[0]
    inputfile = argv[1]
    outputdir = argv[2]
    domainFile = argv[3]
    repName = argv[4:]

    with open( inputfile ) as data_file:

        data = json.load( data_file )

        domainContent = "// File generated by shiftCXX.py. Do not edit.\n"

        for rep in data["reps"] :
            if rep[ "name" ] in repName :
                domainContent += "#include <shift_" + rep[ "name" ] + ".h>\n"

        header_define = "__" + data[ "namespace" ].upper( ).replace("::", "__") + \
                        "__" + data[ "name" ].upper( ) + "__"

        if objectType == "Entity" :
            header_define += "ENTITIES__"
        elif objectType == "Relationship" :
            header_define += "RELATIONSHIPS__"
        domainContent += "#ifndef " + header_define + "\n"
        domainContent += "#define " + header_define + "\n"

        # Namespaces
        namespaces = data[ "namespace" ].split( "::" )
        for namespace in namespaces :
            domainContent += "namespace " + namespace + "\n"
            domainContent += "{\n"

        if objectType == "Entity" :
            domainContent += "class EntitiesTypes : public shift::EntitiesTypes\n" \
                             "{\n" \
                             "public:\n" \
                             "  EntitiesTypes( void )\n" \
                             "  {\n"
            for rep in data["reps"] :
                if rep[ "name" ] in repName :
                    domainContent += "    this->_entitiesTypes.push_back( std::make_tuple( \""  + \
                                     rep[ "name" ] + "\", new " + \
                                     rep[ "namespace" ] + "::" + rep[ "name" ] + ", " + \
                                     str( "subentity" in rep[ "flags" ] ).lower( ) + " ));\n"
            domainContent += "  }\n" \

            domainContent += "  virtual ~EntitiesTypes( void )\n" \
                             "  {}\n"

            domainContent += "};\n"

        if objectType == "Relationship" :
            domainContent += "class RelationshipPropertiesTypes : public shift::RelationshipPropertiesTypes\n" + \
                             "{\n" \
                             "public:\n" \
                             "  RelationshipPropertiesTypes( void )\n" \
                             "  {\n"
            for rep in data["reps"] :
                if rep["name"] in repName:
                    domainContent += "    this->_relationshipPropertiesTypes[\"" + \
                                     rep[ "relationship" ] + "\"] = new " +\
                                     rep[ "namespace" ] + "::" + rep ["name" ] + \
                                     " ;\n"
            domainContent += "  }\n" \

            domainContent += "  virtual ~RelationshipPropertiesTypes( void )\n" \
                             "  {}\n"

            domainContent += "};\n"

        namespaces = data[ "namespace" ].split( "::" )
        for namespace in namespaces :
            domainContent += "}\n"

        domainContent += "#endif\n"


        f = open( domainFile, 'w')
        f.write( domainContent )
        f.close( )

        repsNames = dict( )
        for rep in data["reps"] :
            repsNames[ rep[ "name" ]] = 1;

        for rep in data["reps"] :
            if rep[ "name" ] in repName :
                print_header( objectType, \
                              repsNames, \
                              rep, outputdir + \
                              "/shift_" + rep[ "name" ] + ".h" )
                print_impl( objectType, \
                            rep, outputdir + "/shift_" + rep[ "name" ] + \
                            ".cpp" );

if __name__ == "__main__":
    main( sys.argv[1:] )
