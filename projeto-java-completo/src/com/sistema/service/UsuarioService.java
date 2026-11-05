package com.sistema.service;

import com.sistema.model.Usuario;
import java.util.ArrayList;
import java.util.List;

public class UsuarioService {
    private final List<Usuario> usuarios = new ArrayList<>();

    public void salvar(Usuario usuario) {
        usuarios.add(usuario);
    }

    public List<Usuario> listarTodos() {
        return usuarios;
    }
}
