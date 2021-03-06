import java.io.*;
import java.util.Arrays;
import java.util.Locale;
import java.util.StringTokenizer;

public class MergingTables {
    private final InputReader reader;
    private final OutputWriter writer;
    private int[] id;	// parent[i] = parent of i
    private Table[] tables;
    private int[] rank;

    public MergingTables(InputReader reader, OutputWriter writer) {
        this.reader = reader;
        this.writer = writer;
    }

    public static void main(String[] args) {
        InputReader reader = new InputReader(System.in);
        OutputWriter writer = new OutputWriter(System.out);
        new MergingTables(reader, writer).run();
        writer.writer.flush();
    }

    class Table {
        Table parent;
        int numberOfRows;
        int i;
        
        
        Table(int numberOfRows, int i) {
            this.numberOfRows = numberOfRows;
            parent = this;
            //grandparent = null;
            this.i = i;
            
        }
        int getParent() {
            // find super parent and compress path
            
        	int root = this.i;
            while (root != id[root])
                root = id[root];
            while (this.i != root) {
                int newp = id[this.i];
                id[this.i] = root;
                this.i = newp;
            }
            return root;
        	
        	
        }
    }

    int maximumNumberOfRows = -1;

    void merge(Table destination, Table source) {
        int realDestination = destination.getParent();
        int realSource = source.getParent();
        if (realDestination == realDestination) {
            return;
        }
        
        /*int rootP = find(p);
        int rootQ = find(q);
        if (rootP == rootQ) return;

        // make root of smaller rank point to root of larger rank
        if      (rank[rootP] < rank[rootQ]) parent[rootP] = rootQ;
        else if (rank[rootP] > rank[rootQ]) parent[rootQ] = rootP;
        else {
            parent[rootQ] = rootP;
            rank[rootP]++;
        }
        count--;*/
        
        
        
        
        if      (rank[realDestination] < rank[realSource]) {
            id[realDestination] = realSource;
            
            tables[realDestination].numberOfRows = tables[destination.i].numberOfRows + tables[source.i].numberOfRows;
            tables[source.i].numberOfRows = 0;
            maximumNumberOfRows = Math.max(maximumNumberOfRows, tables[realDestination].numberOfRows);
        }
        else if (rank[realDestination] > rank[realSource]) {
            id[realSource] = realDestination;
            
            tables[realSource].numberOfRows = tables[destination.i].numberOfRows + tables[source.i].numberOfRows;
            tables[destination.i].numberOfRows = 0;
            maximumNumberOfRows = Math.max(maximumNumberOfRows, tables[realSource].numberOfRows);
        }
        else {
            id[realSource] = realDestination;
            rank[realDestination]++;
            
            tables[realSource].numberOfRows = tables[destination.i].numberOfRows + tables[source.i].numberOfRows;
            tables[destination.i].numberOfRows = 0;
            maximumNumberOfRows = Math.max(maximumNumberOfRows, tables[realSource].numberOfRows);
        }
        
        // merge two components here
        // use rank heuristic
        // update maximumNumberOfRows
    }

    public void run() {
        int n = reader.nextInt();
        int m = reader.nextInt();
        tables = new Table[n];
        id = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) {
            int numberOfRows = reader.nextInt();
            tables[i] = new Table(numberOfRows, i);
            maximumNumberOfRows = Math.max(maximumNumberOfRows, numberOfRows);
            id[i] = i;
            rank[i] = 0;
        }
        for (int i = 0; i < m; i++) {
            int destination = reader.nextInt() - 1;
            int source = reader.nextInt() - 1;
            merge(tables[destination], tables[source]);
            writer.printf("%d\n", maximumNumberOfRows);
        }
    }


    static class InputReader {
        public BufferedReader reader;
        public StringTokenizer tokenizer;

        public InputReader(InputStream stream) {
            reader = new BufferedReader(new InputStreamReader(stream), 32768);
            tokenizer = null;
        }

        public String next() {
            while (tokenizer == null || !tokenizer.hasMoreTokens()) {
                try {
                    tokenizer = new StringTokenizer(reader.readLine());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            return tokenizer.nextToken();
        }

        public int nextInt() {
            return Integer.parseInt(next());
        }

        public double nextDouble() {
            return Double.parseDouble(next());
        }

        public long nextLong() {
            return Long.parseLong(next());
        }
    }

    static class OutputWriter {
        public PrintWriter writer;

        OutputWriter(OutputStream stream) {
            writer = new PrintWriter(stream);
        }

        public void printf(String format, Object... args) {
            writer.print(String.format(Locale.ENGLISH, format, args));
        }
    }
}
