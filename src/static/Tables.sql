CREATE TABLE `users` (
  `id` VARCHAR(36) PRIMARY KEY,
  `email` VARCHAR(120) UNIQUE NOT NULL,
  `first_name` VARCHAR(64) NOT NULL,
  `last_name` VARCHAR(64) NOT NULL,
  `password_hash` VARCHAR(128) NOT NULL,
  `is_admin` BOOLEAN DEFAULT false,
  `created_at` TIMESTAMP DEFAULT (current_timestamp),
  `updated_at` TIMESTAMP DEFAULT (current_timestamp)
);

CREATE TABLE `amenities` (
  `id` VARCHAR(36) PRIMARY KEY,
  `name` VARCHAR(128) NOT NULL,
  `created_at` TIMESTAMP DEFAULT (current_timestamp),
  `updated_at` TIMESTAMP DEFAULT (current_timestamp)
);

CREATE TABLE `cities` (
  `id` VARCHAR(36) PRIMARY KEY,
  `name` VARCHAR(128) NOT NULL,
  `country_code` VARCHAR(36) NOT NULL,
  `created_at` TIMESTAMP DEFAULT (current_timestamp),
  `updated_at` TIMESTAMP DEFAULT (current_timestamp)
);

CREATE TABLE `countries` (
  `code` VARCHAR(36) PRIMARY KEY,
  `name` VARCHAR(128) NOT NULL
);

CREATE TABLE `places` (
  `id` VARCHAR(36) PRIMARY KEY,
  `name` VARCHAR(128) NOT NULL,
  `description` TEXT,
  `address` VARCHAR(256) NOT NULL,
  `latitude` FLOAT NOT NULL,
  `longitude` FLOAT NOT NULL,
  `host_id` VARCHAR(36),
  `city_id` VARCHAR(36),
  `price_per_night` INT NOT NULL,
  `number_of_rooms` INT NOT NULL,
  `number_of_bathrooms` INT NOT NULL,
  `max_guests` INT NOT NULL,
  `created_at` TIMESTAMP DEFAULT (current_timestamp),
  `updated_at` TIMESTAMP DEFAULT (current_timestamp)
);

CREATE TABLE `reviews` (
  `id` VARCHAR(36) PRIMARY KEY,
  `comment` TEXT NOT NULL,
  `rating` INT NOT NULL,
  `user_id` VARCHAR(36),
  `place_id` VARCHAR(36),
  `created_at` TIMESTAMP DEFAULT (current_timestamp),
  `updated_at` TIMESTAMP DEFAULT (current_timestamp)
);

ALTER TABLE `places` ADD FOREIGN KEY (`host_id`) REFERENCES `users` (`id`);

ALTER TABLE `places` ADD FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`);

ALTER TABLE `reviews` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `reviews` ADD FOREIGN KEY (`place_id`) REFERENCES `places` (`id`);

ALTER TABLE `cities` ADD FOREIGN KEY (`country_code`) REFERENCES `countries` (`code`);

ALTER TABLE `reviews` ADD FOREIGN KEY (`place_id`) REFERENCES `reviews` (`rating`);

ALTER TABLE `users` ADD FOREIGN KEY (`first_name`) REFERENCES `amenities` (`id`);
