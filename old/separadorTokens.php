<?php

class TokenSeparator {

    private $_filePath;
    private $_fpInputFile;
    private $_inputFileContent;
    private $_currentLineNumber;
    private $_currentLine;
    private $_specialTokensList;
    private $_keyWords;

    public function __construct()
    {
        $this->_keyWords = array();
        $this->_specialTokensList = array();
        $this->_currentLineNumber = 0;
    }

    public function loadKeyWords($keyWordsFilePath)
    {
        $fileContent = file_get_contents($keyWordsFilePath);

        $listOfKeyWords = json_decode($fileContent);

        $this->_keyWords = array_merge(
            $this->_keyWords,
            $listOfKeyWords
        );
    }

    public function loadSpecialTokens($specialTokensFilePath)
    {
        $fileContent = file_get_contents($specialTokensFilePath);
        
        $listOfSpecialTokens = json_decode($fileContent);

        $this->_specialTokensList = array_merge(
            $this->_specialTokensList,
            $listOfSpecialTokens
        );
    }

    public function cleanKeyWorkds()
    {
        $this->_keyWords = array();
    }

    public function setInputFile($filePath){
        if(!is_file($filePath)){
            throw new Exception("Invalid input file specified");
        } 

        $this->_filePath = $filePath;
    }

    public function openInputFile(){
        $fp = fopen($this->_fpInputFile, "r");

        if(empty($fp)){
            throw new Exception("Opening input file failed");
        }
        
        $this->_fpInputFile = $fp;
    }

    public function closeInputFile(){
        fclose($this->_fpInputFile);
        $this->_fpInputFile = null;
    }

    public function readLine(){
        $this->_currentLine = fgets($this->_fpInputFile);
        $this->_currentLineNumber++;

        return $this->_currentLine;
    }

    public function splitTokens()
    {
        
    }

    private function _readChar($line){
        
    }

    public function readInputFile(){
        
    }
}

class TokenBuilder {
    
    private $_currentState;
    private $_tokenChars;     

    public function consume($char){

    }



}

$content = file_get_contents("program.c");
echo $content;