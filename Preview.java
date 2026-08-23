/**
 * Preview file for the retro IDE color schemes.
 *
 * Open this file with each scheme to check Java coverage:
 * Javadoc, annotations, generics, fields, local variables, and enums.
 *
 * @author Custom
 * @see Money#add(Money)
 */
package com.example.retro;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.function.Function;

@FunctionalInterface
interface Rounder {
    double round(double value);
}

enum Currency {
    EUR("€"),
    USD("$");

    private final String symbol;          // private field

    Currency(String symbol) {
        this.symbol = symbol;
    }

    public String symbol() {
        return this.symbol;
    }
}

public final class Money implements Comparable<Money> {

    public static final int MAX_RETRY = 3;         // static final field
    private static final double RATE = 0.075D;
    private static final long MASK = 0xFF00L;

    private final double amount;
    private final Currency currency;

    public Money(double amount, Currency currency) {
        if (amount < 0.0) {
            throw new IllegalArgumentException("negative amount: " + amount);
        }
        this.amount = amount;
        this.currency = Objects.requireNonNull(currency, "currency");
    }

    /**
     * Adds two amounts of the same currency.
     *
     * @param other the other amount
     * @return the sum
     * @throws IllegalStateException if the currencies do not agree
     */
    public Money add(Money other) {
        // TODO: support more than one currency
        if (this.currency != other.currency) {
            throw new IllegalStateException("currency mismatch");
        }
        return new Money(this.amount + other.amount, this.currency);
    }

    @Override
    public int compareTo(Money other) {
        return Double.compare(this.amount, other.amount);
    }

    @Override
    public String toString() {
        return String.format("%.2f%s", this.amount, this.currency.symbol());
    }

    @Deprecated
    public double legacyValue() {
        return this.amount * (1.0 - RATE);
    }

    public static <T extends Number> double sum(List<T> values, Function<T, Double> map) {
        double total = 0.0;
        for (T value : values) {
            total += map.apply(value);
        }
        return total;
    }

    public static void main(String... args) {
        List<Money> items = new ArrayList<>();
        items.add(new Money(19.99, Currency.EUR));
        items.add(new Money(5.01, Currency.EUR));

        Money total = items.stream()
                .reduce(new Money(0.0, Currency.EUR), Money::add);

        Rounder rounder = value -> Math.round(value * 100.0) / 100.0;
        System.out.println(total + " mask=" + MASK + " retry=" + MAX_RETRY);
        System.out.printf("rounded=%s%n", rounder.round(total.legacyValue()));

        char tab = '\t';
        String text = """
                A text block
                with a second line.""";
        assert !text.isEmpty() : "empty" + tab;
    }
}
