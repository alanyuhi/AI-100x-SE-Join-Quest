@double11
Feature: Double 11 Promotion
  As a shopper
  I want the system to apply Double 11 discounts for bulk purchases of the same product
  So that I can enjoy special savings during the Double 11 event

  Scenario: Buy 12 pairs of socks at 100 each
    Given the double 11 promotion is active
    When a customer places an order with:
      | productName | quantity | unitPrice |
      | 襪子          | 12       | 100       |
    Then the order summary should be:
      | totalAmount |
      | 1000        |

  Scenario: Buy 27 pairs of socks at 100 each
    Given the double 11 promotion is active
    When a customer places an order with:
      | productName | quantity | unitPrice |
      | 襪子          | 27       | 100       |
    Then the order summary should be:
      | totalAmount |
      | 2300        |

  Scenario: Buy 10 different products at 100 each
    Given the double 11 promotion is active
    When a customer places an order with:
      | productName | quantity | unitPrice |
      | A           | 1        | 100       |
      | B           | 1        | 100       |
      | C           | 1        | 100       |
      | D           | 1        | 100       |
      | E           | 1        | 100       |
      | F           | 1        | 100       |
      | G           | 1        | 100       |
      | H           | 1        | 100       |
      | I           | 1        | 100       |
      | J           | 1        | 100       |
    Then the order summary should be:
      | totalAmount |
      | 1000        | 