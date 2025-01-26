package com.XmasWish;

import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.model.rest.RestBindingMode;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.Bean;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

import com.XmasWish.model.XmasWish;
import java.util.List;

@SpringBootApplication
@EnableJpaRepositories(basePackages = "com.XmasWish.model")
@EntityScan(basePackages = "com.XmasWish.model")
public class YourApplication {

    public static void main(String[] args) {
        SpringApplication.run(YourApplication.class, args);
    }

    @Bean
    RouteBuilder restRoute() {
        return new RouteBuilder() {

            @Override
            public void configure() throws Exception {

                // REST configuration
                restConfiguration()
                        .component("netty-http")
                        .host("0.0.0.0")
                        .port(8086)
                        .bindingMode(RestBindingMode.json);

                // Define REST endpoint
                rest()
                        .get("/submitWish").produces("text/html").to("direct:serveMakeWish")
                        .get("/uploadWish").produces("text/html").to("direct:serveUploadWish")
                        .post("/api/wish").type(XmasWish.class).to("direct:saveToH2");

                from("direct:serveMakeWish")
                        .setHeader("Content-Type", constant("text/html"))
                        .transform().constant("resource:classpath:static/makeWish.html");

                from("direct:serveUploadWish")
                        .setHeader("Content-Type", constant("text/html"))
                        .transform().constant("resource:classpath:static/uploadWish.html");

                from("direct:saveToH2")
                        .process(exchange -> {
                            XmasWish wish = exchange.getIn().getBody(XmasWish.class);
                            exchange.setProperty("name", wish.getName());
                            exchange.setProperty("wish", wish.getWish());
                            exchange.setProperty("status", wish.getStatus());
                        })
                        .to("sql:INSERT INTO XMAS_WISH (name, wish, status) VALUES (:#${exchangeProperty.name}, :#${exchangeProperty.wish}, :#${exchangeProperty.status})?dataSource=#dataSource")
                        .setBody(simple("${exchangeProperty.name}"));

            }
        };
    }
}

// mvn spring-boot:run