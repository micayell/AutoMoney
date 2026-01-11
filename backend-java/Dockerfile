FROM eclipse-temurin:17-jdk-alpine
VOLUME /tmp
COPY . .
RUN ./gradlew build -x test || return 0 
# Note: Since there is no gradlew in the repo, we might need a base image with gradle or rely on the user having it.
# However, the user agreed to use Docker because they don't have gradle.
# So we need a base image that HAS gradle.

FROM gradle:8.5-jdk17-alpine AS build
COPY --chown=gradle:gradle . /home/gradle/src
WORKDIR /home/gradle/src
RUN gradle build --no-daemon -x test

FROM eclipse-temurin:17-jre-alpine
EXPOSE 8080
COPY --from=build /home/gradle/src/build/libs/*.jar app.jar
ENTRYPOINT ["java","-jar","/app.jar"]

