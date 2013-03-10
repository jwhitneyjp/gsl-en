# Copyright 2007 by Starling Software, K.K.
# This is part of QAM from http://www.starling-software.com.
# For license terms, see the LICENSE.QAM file included with this distribution.

module Enumerable

    def take_while
	inject([]) { |memo, el|
	    yield(el) ? (memo << el) : (return memo)
	}
    end

end

class Array

    def drop_while
	i = 0
	i += 1 while i < length && yield(self[i])
	self[i..-1]
    end

end

class Object

    def append_message_and_raise(exception, message)
	e2 = exception.class.new(exception.message + message)
	e2.set_backtrace(exception.backtrace)
	raise e2
    end

end

class Class

    def initialize_vars(*vars, &initialize_block)
	vars.each { |arg| attr_reader arg.to_sym }
	varsyms = vars.collect { |arg| ('@' + arg.to_s).to_sym }
	define_method(:initialize) { |*init_args|
	    raise(ArgumentError, "wrong number of arguments " +
		"(#{init_args.length} for #{vars.length})") unless
		vars.length == init_args.length
	    vars.zip(init_args).each { |var, arg|
		instance_variable_set(('@' + var.to_s).to_sym, arg)
	    }
	    self.instance_eval(&initialize_block) if initialize_block
	}
    end

end

class Module

    def class_constant(name, initval)
	const_set(name, initval) unless constants.include?(name.to_s)
	yield(const_get(name)) if block_given?
    end

end
