class RegexTester
    def initialize(pattern=nil)
      @pattern = pattern unless pattern.nil?
    end

    attr_accessor :pattern

    def statement=(statement)
        @statement = statement
      end

    def statement
        @statement
    end

    def test
        if pattern_matches? @statement
          puts "MATCH: #{@statement}"
        else
          STDERR.puts "NO MATCH: #{@statement}"
        end
      end 

    private
    def pattern_matches? statement
        statement.match(@pattern) != nil
    end

  end

  regex = RegexTester.new
  regex.pattern = /^(http:\/\/)?www\.\w+\.(com|edu|org)$/  # from test_arrays.rb
  puts regex.pattern
  regex.statement = "http://www.google.com"
  puts regex.statement
  puts "------"
  regex.test
  regex.statement = "apidock.com"
  regex.test
