package demo;

import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;



public class FactorialTest {

    @Test
    void testNegative() {
        assertThrows(IllegalArgumentException.class, new Executable() {
            @Override
            public void execute() throws Throwable {
                Factorial.fact(-1);
            }
        });
    }
}