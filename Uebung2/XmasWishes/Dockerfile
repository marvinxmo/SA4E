# Stage 1: Build the application
FROM maven:3.8.5-openjdk-17 AS build

# Set the working directory
WORKDIR /app

# Copy the pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline

# Copy the source code and build the application
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Run the application
FROM openjdk:17-jdk-slim

# Set the working directory
WORKDIR /app

# Copy the built application from the previous stage
COPY --from=build /app/target/*.jar app.jar

# Expose the application port
EXPOSE 8085
EXPOSE 8086

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
