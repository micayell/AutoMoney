package com.automoney.dto;

import lombok.Getter;
import lombok.Setter;

@Getter @Setter
public class AuthDto {
    
    @Getter @Setter
    public static class LoginRequest {
        private String username;
        private String password;
    }

    @Getter @Setter
    public static class SignupRequest {
        private String username;
        private String password;
        private String email;
    }

    @Getter @Setter
    public static class TokenDto {
        private String token;

        public TokenDto(String token) {
            this.token = token;
        }
    }
}

