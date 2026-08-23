/* Preview file for the retro IDE color schemes.
 *
 * Open this file with each scheme to check C coverage:
 * preprocessor directives, macros, types, strings, and escapes.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RETRY 3
#define SQUARE(x) ((x) * (x))          /* macro with parameters */

#ifdef DEBUG
#define LOG(fmt, ...) fprintf(stderr, "[log] " fmt "\n", __VA_ARGS__)
#else
#define LOG(fmt, ...) ((void) 0)
#endif

static const double RATE = 0.075;
static const unsigned MASK = 0xFF00u;
static const char *const GREETING = "Total:\t%.2f %s\n";

typedef enum Currency { CURRENCY_EUR = 0, CURRENCY_USD } Currency;

typedef struct Money {
    double amount;
    Currency currency;
    char label[32];
} Money;

static Money money_make(double amount, Currency currency)
{
    Money money = { .amount = amount, .currency = currency };
    snprintf(money.label, sizeof money.label, "%.2f", amount);
    return money;
}

static int money_add(Money *out, const Money *a, const Money *b)
{
    if (out == NULL || a == NULL || b == NULL) {
        return -1;                     /* invalid argument */
    }
    if (a->currency != b->currency) {
        LOG("currency mismatch: %d vs %d", a->currency, b->currency);
        return -2;
    }
    *out = money_make(a->amount + b->amount, a->currency);
    return 0;
}

int main(int argc, char **argv)
{
    Money a = money_make(19.99, CURRENCY_EUR);
    Money b = money_make(5.01, CURRENCY_EUR);
    Money sum;

    /* TODO: read the amounts from the command line */
    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "--verbose") == 0) {
            LOG("argument %d: %s", i, argv[i]);
        }
    }

    if (money_add(&sum, &a, &b) != 0) {
        fputs("failed\n", stderr);
        return EXIT_FAILURE;
    }

    printf(GREETING, sum.amount * (1.0 - RATE), "EUR");
    printf("square=%u mask=%#x retry=%d\n", SQUARE(4u), MASK, MAX_RETRY);
    return EXIT_SUCCESS;
}
