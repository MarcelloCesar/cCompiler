package Atividade1;
import java.util.Date;

public class Cliente {
    private String nome;
    private int idade;
    private Date dtNasc;           
    private String sexo;
    private String cidade;
    private int salario;

    public String getSexo() {
        return sexo;
    }

    public void setSexo(String sexo) {
        this.sexo = sexo;
    }

    public String getCidade() {
        return cidade;
    }

    public void setCidade(String cidade) {
        this.cidade = cidade;
    }

    public int getSalario() {
        return salario;
    }

    public void setSalario(int salario) {
        this.salario = salario;
    }
    
    public String getNome(){
        return nome;
    }
    
    public void setNome(String nome){
        this.nome = nome;
    }
    
    public int getIdade(){
        return idade;
    }
    
    public void setIdade(int idade){
        this.idade = idade;
    }
    
    public Date getDtNasc(){
        return dtNasc;
    }
    
    public void setDtNasc(Date DataNasc){
        this.dtNasc = DataNasc;
    }
}
