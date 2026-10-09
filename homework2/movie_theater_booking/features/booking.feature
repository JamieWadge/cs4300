Feature: Booking movie seats
  As a moviegoer
  I want to browse movies, book seats and review my bookings
  So that I can plan my night out

  Background:
    Given a movie called "Small Planets"
    And a seat "A1"
    And a seat "A2"
    And a registered user "ann"

  Scenario: Anyone can browse the movie list
    Given I am not logged in
    When I visit the movie list
    Then I should see "Small Planets"

  Scenario: Anonymous visitors must log in to book
    Given I am not logged in
    When I open the booking page for "Small Planets"
    Then I should be redirected to the login page

  Scenario: A logged-in user books a seat
    Given I am logged in as "ann"
    When I book seat "A1" for "Small Planets"
    Then I should see "Seat A1 booked for Small Planets"
    And seat "A1" should be unavailable
    And "ann" should have 1 booking

  Scenario: A booked seat cannot be booked again
    Given a registered user "bob"
    And seat "A1" is already booked by "bob" for "Small Planets"
    And I am logged in as "ann"
    When I book seat "A1" for "Small Planets"
    Then I should see "Choose an available seat"
    And "ann" should have 0 bookings

  Scenario: Booking history shows only my bookings
    Given a registered user "bob"
    And seat "A1" is already booked by "bob" for "Small Planets"
    And I am logged in as "ann"
    When I open my booking history
    Then I should see "You haven't booked anything yet"

  Scenario: Cancelling a booking frees the seat
    Given I am logged in as "ann"
    And I book seat "A2" for "Small Planets"
    When I cancel my booking for seat "A2"
    Then I should see "Booking cancelled"
    And seat "A2" should be available
