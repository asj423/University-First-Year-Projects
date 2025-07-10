import java.io.BufferedReader;
import java.io.FileReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.FileNotFoundException;
import java.io.IOException;

public class PopThread implements Runnable{
    private static final String outputFile = "result.txt";
    private static int count = 1;
    private final ArrayList<String> fileList;
    private static int runningThreads = 0;
    
    public PopThread(ArrayList<String> fileList) {
        this.fileList = fileList;
        synchronized (PopThread.class){
            runningThreads++;
        }
    }
    
   public void run(){
       
       if(count == 1){
           clearFile();
       }
       
        for(String fileName : fileList){
            String fileContent = readFile(fileName);
            int fileLabel = getLabel(fileContent);
            
            synchronized (PopThread.class) {
                while (fileLabel != count) {
                    try {
                        PopThread.class.wait(1000);  
                    } 
                    catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }

                writeFile(fileContent); 
                count++;  
                PopThread.class.notifyAll();
            }
        }
        synchronized (PopThread.class){
            runningThreads--;
            if(runningThreads == 0){
                count = 1;
                PopThread.class.notifyAll();
            }
        }
    }
    
    private String readFile(String filename){
        String line;
        String wholeFile = "";
        BufferedReader br;
        try {
            br = new BufferedReader(new FileReader(filename));
            while((line = br.readLine()) != null){
                wholeFile += line + "\n";
            }
            return wholeFile.trim();
        }
        catch(FileNotFoundException e) {
            return("File not found: " + filename);
        }
        catch(IOException e){
            return("Error reading file: " + e.getMessage());
        }
    }    
    
    private void writeFile(String content) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(outputFile, true))) {
            bw.write(content);
            bw.newLine();
        } 
        catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    private int getLabel(String content){
        for (int i = content.length() - 4; i >= 0; i--) {
            
            if (content.charAt(i) == '#') {
                
                if (Character.isDigit(content.charAt(i + 1)) && Character.isDigit(content.charAt(i + 2)) && Character.isDigit(content.charAt(i + 3))) {
                    String labelSubstring = content.substring(i + 1, i + 4);
                    return Integer.parseInt(labelSubstring);
                }
            }
        }
        return -1;
    }
    
    public void clearFile(){
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(outputFile, false))) {
            bw.write("");
        } 
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}
