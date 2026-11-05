package com.sistema;

import com.sistema.controller.UsuarioController;

public class Main {
    public static void main(String[] args) {
        System.out.println("Sistema Java Inicializado!");
        UsuarioController controller = new UsuarioController();
        controller.executar();
    }
}
