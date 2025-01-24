package com.example;

import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.model.rest.RestBindingMode;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import com.example.model.Message;

@SpringBootApplication
public class YourApplication {

    public static void main(String[] args) {
        SpringApplication.run(YourApplication.class, args);
    }

    @Bean
    RouteBuilder restRoute() {
        return new RouteBuilder() {
            @Override
            public void configure() throws Exception {
                restConfiguration()
                        .component("undertow")
                        .host("0.0.0.0")
                        .port(8082)
                        .bindingMode(RestBindingMode.json);

                rest("/api")
                        .post("/echo")
                        .type(Message.class)
                        .to("direct:echoMessage");

                rest()
                        .get("/")
                        .produces("text/html")
                        .to("direct:serveHtml");

                from("direct:serveHtml")
                        .setHeader("Content-Type", constant("text/html"))
                        .setBody().simple("resource:classpath:static/index.html");

                from("direct:echoMessage")
                        .log("Received message: ${body.content}")
                        .setBody(simple("${body}"));
            }
        };
    }
}