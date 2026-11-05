package com.sistema.controller;

import com.sistema.model.Usuario;
import com.sistema.service.UsuarioService;

public class UsuarioController {
    private final UsuarioService service = new UsuarioService();

    public void executar() {
        service.salvar(new Usuario(1L, "Teste Dev", "dev@empresa.com"));
        System.out.println("Usuarios cadastrados: " + service.listarTodos().size());
    }
}
