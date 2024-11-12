from conexao import conectar, messagebox

# Função para inserir uma nova despesa no banco de dados
def inserir_despesa(valor, categoria, data, descricao):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO despesas (valor, categoria, data, descricao)
            VALUES (%s, %s, %s, %s)
        """, (valor, categoria, data, descricao))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Despesa adicionada com sucesso!")

# Função para listar despesas
def listar_despesas():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM despesas")
        despesas = cursor.fetchall()
        conn.close()
        return despesas
    else:
        return []

# Função para remover uma despesa pelo ID
def remover_despesa(despesa_id):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM despesas WHERE id = %s", (despesa_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Despesa removida com sucesso!")

# Função para atualizar uma despesa no banco de dados
def atualizar_despesa(despesa_id, valor, categoria, data, descricao):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE despesas 
            SET valor = %s, categoria = %s, data = %s, descricao = %s
            WHERE id = %s
        """, (valor, categoria, data, descricao, despesa_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Despesa atualizada com sucesso!")