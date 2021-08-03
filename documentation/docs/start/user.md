# User Worlflow

<!-- load mermaid -->
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
mermaid.initialize({startOnLoad:true});
mermaidAPI.initialize({
    securityLevel: 'loose'
});
</script>

**Pro Tip**: Clicking on the purple nodes leads to the specific step in the documentation.
<!-- **Pro Tip**: Clicking on the purple nodes leads to the tool page. -->

<div class="mermaid">
graph TD
    subgraph Dataset Prep page
    A[time-series excel workbook OR structural data csv files]
    end
    subgraph Model page
    B[Unemployment Rate Prediction on Kreis-level]
    C[Visualization: line plot, map of Germany]
    D[Output file: single excel worksheet]
    B --> C --> D
    end
    subgraph Error Analysis page
    E[Compare: structural, crisis-time data]
    end
    subgraph Home page
    F[Rankings & Groupings]
    end
    A --> B
    D --> E
    D --> F
    click A "../../steps/data_prep/"
    click B "../../steps/model/#fit-model-and-export-predictions"
    click C "../../steps/model/#visualize-prediction-results"
    click E "../../steps/error/"
    click F "../../steps/home/"
</div>