class cmd:
    """
    Class to represent a command
    """

    def __init__(self):
        """
        The constructor

        TODO : Add parameters
        """
	self.NAME=""
    	self.SHORT_NAME=""
    	self.DESCRIPTION=""
    	self.EXAMPLES=[]
    	self.VALID_OPTIONS={}
    	self.VALID_OPTION_NAMES=[]
    	self.VALID_OPTION_SHORT_NAMES=[]
    	self.HANDLER=None
        return None
    
    def setName(self, name: str):
        """
        Set long command name

        @param name (str) The command name

        @return True is success

        TODO : Add more checks
        """
        if len(name) > 0:
            self.NAME = name
            return True
        else:
            return False

    def setShortName(self, short_name: str ):
        """
        Set short command name

        @param short_name (str) The command short name

        @return True if success

        TODO : Add more checks
        """
        if len(short_name) > 0:
            self.SHORT_NAME = short_name
            return True
        else:
            return False
    
    def setDescription(self, description: str ):
        """
        Set the description

        @param description (str) The command description

        @return True if success

        TODO : Add more checks here
        """
        if len(description) > 0:
            self.DESCRIPTION = description
            return True
        else:
            return False

    def addOption(self, name: str, short_name: str, desc: str, typ: list, req: bool, ex ):
        """
        Add a command option

        @param name (str) option name
        @param desc (str) option description
        @param typ  (list) list of valid value types for this option
        @param req  (boolean) is the option mandatory
        @param ex   (any) an example value

        @return True if success

        TODO : Add checks here
        """
        # Option already exists, fail operation
        if name in self.VALID_OPTION_NAMES:
            return False

        self.VALID_OPTIONS[name] = { "shortName" : short_name, "description" : desc, "type" : typ, "required" : req, "exVal" : ex }
        self.VALID_OPTION_NAMES.append( name )
        self.VALID_OPTION_SHORT_NAMES.append( short_name )
        return True

    def addExample(self, ex: str, desc: str ):
        """
        Add a command usage example

        @param ex (str) Example string
        @param desc (str) example description

        @return True if success

        TODO : Add checks here
        """
        self.EXAMPLES.append( { "exampleStr" : ex, "description" : desc } )
        return True

    def setHandler(self, handler):
        """
        Add a command handler function

        @param handler (function) Handler function

        @return True

        TODO : Add checks here
        """
        self.HANDLER = handler
        return True

    def optionValid( self, option: dict ):
        """
        Validate an option
    
        @param option (dict) : { "<option full name>" : value(s) } Option object

        @return True if option is valid
        """
        name = list(option.keys())[0]
        if name in self.VALID_OPTION_NAMES:
            option_name = name
        elif name in self.VALID_OPTION_SHORT_NAMES:
            option_name = self.VALID_OPTION_NAMES[ self.VALID_OPTION_SHORT_NAMES.index(name) ]
        else:
            return False

        vals = option[name]
        for val in vals:
            if type(val) not in self.VALID_OPTIONS[option_name]["type"]:
                return False
        
        return True

    def execute( self, options: dict ):
        """
        Execute the command

        @param options (dict) { option1 : [vals] , option2 : [vals] ... } List of option objects

        @return Handler return object upon successful execution, None otherwise

        @note DONOT return None object from the handler.
        """
        if self.HANDLER == None:
            return None

        # Validate the options
        for option in list(options.keys()):
            if self.optionValid( { option : options[option] } ) == False:
                return None

        return self.HANDLER( options )

    def help( self, toolName: str ):
        """
        Return the help string for the command

        @param toolName Name of the tool

        @return Help string
        """
        helpStr = "* {}\n".format( self.NAME )
        helpStr += "{}\n\n".format(self.DESCRIPTION)
        helpStr += "{} {} [options] \n".format( toolName, self.NAME )
        helpStr += "OR\n{} {} [options] \n\n".format( toolName, self.SHORT_NAME )
        
        helpStr += "Options : \n"
        for option in self.VALID_OPTION_NAMES:
            if self.VALID_OPTIONS[option]["required"] == True:
                helpStr += "\t{}: Mandatory, ex: {}\n".format( option, self.VALID_OPTIONS[option]["exVal"] )
            else:
                helpStr += "\t{} : Optional\n".format( option )
            
            helpStr += "\t{}\n\n".format( self.VALID_OPTIONS[option]["description"] )
        
        helpStr += "Examples:\n"
        for ex in self.EXAMPLES:
            helpStr += "\t{}\n\t{}\n\n".format( ex["exampleStr"], ex["description"] )

        return helpStr
