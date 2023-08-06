
import logging as log

log.basicConfig(level=log.INFO)

class Rule():
    def __init__(self):
        """
            Description:
                Initialize Rule class
            
            Example:
                Rule()
            
            Returns:
                None

        """
        self.state = {} 
        pass

    def setState(self, key, value):
        """
            Description:
                Set state of key
            
            Example:
                setState(key, value)
            
            Returns:
                None
        """
        self.state[key] = value
        pass

    def getState(self, key):
        """
            Description:
                Get state of key
            
            Example:
                getState(key)
            
            Returns:
                Any
        """
        return self.state[key]

    def getlist(self, *args):
        """
            Description:
                Get list of args
            
            Example:
                getlist({data, columns, state, derive, _validate, trigger, condition})
            
            Returns:
                List
        """
        ls = []
        data, columns = args
        for row in data:
            log.info(row)
            for column in columns:
                ls.append(row[column])
        return ls

    def _validate(self, *args):
        """
            Description:
                _Validate args
            
            Example:
                _validate({data, columns, state, derive,  trigger, condition})
            
            Returns:
                Any
            
        """
        condition, trigger, formula, derive,  data, columns, state = args
        try:
            assert data == list or None
            assert columns == list or None
            assert derive == object or bool or None
            assert formula == function or None
            assert trigger == function or None
            assert condition == function or None
            assert state == str or None
        except Exception as e:
            raise ValueError(e)

    async def decide(self, *args, **kwargs):
        """ 
            Description:
                Execute decide and take a next rule action

            Example:
                decide({data, columns, state, derive, _validate, trigger, condition})

            Returns:
                Any | None
        """
        self._validate(*args)
        ls, derive, condition, formula, trigger, state = {
            args, self.getlist(args)}
        if derive is function and not None:
            condition = condition & derive()
        if derive is object and not None:
            self.state.update(dict(derive)["state"])
            condition = condition(dict(derive)[state])
        if condition:
            res = formula(ls, **kwargs)
            self.setState(state, res)
            if trigger is not None:
                trigger(res)
            return res
        pass

    async def watchState(self, object: object, states, trigger: function):
        """ 
            Description:
                Watch state of object and execute trigger

            Example:
                watchState(object, state, trigger)

            Returns:
                DYN: RESULT
        """
        for state in states:
            currentstate = dict(object)[state]
            objectname = object.__name__
            objectstate = objectname+"_"+state
            self.setState(objectstate, currentstate)

            while True:
                if self.getState(objectstate) != currentstate:
                    yield trigger()
                pass

 
        

