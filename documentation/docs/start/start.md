# Start Here

<!-- load mermaid -->
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>
mermaid.initialize({startOnLoad:true});
mermaidAPI.initialize({
    securityLevel: 'loose'
});
</script>

*We have identified four potential types of users that would benefit from this documentation and tool. If you have a suggestion of another type of user we did not think of, please let us know.*

[🤯 First-time Users](#first-time-users) |
[😊 Experienced Users](#experienced-users) |
[😅 Quick Access](#quick-access) |
[🤔 Technical Users](#technical-users)

**Pro Tip**: Clicking on the blue boxes in the flowchart brings you to the documentation page for that specific step.

## First-time Users

This is a simplified version of the user workflow. You can find the detailed [user workflow](../../start/user/) here.

<!-- <div class="mermaid">
graph LR
    subgraph Dataset Prep page
    A[data input]
    end
    subgraph Model page
    B[prediction]
    end
    subgraph Error Analysis page
    E[compare results]
    end
    subgraph Home page
    F[data story-telling]
    end
    F -.-> A
    A -.-> B
    B -.-> E
    B -.-> F
    click A "https://github.com/prakharrathi25/the-tool-bmwi/blob/main/pages/data_prep.py"
    click B "https://github.com/prakharrathi25/the-tool-bmwi/blob/main/pages/model_v1.py"
    click E "https://github.com/prakharrathi25/the-tool-bmwi/blob/main/pages/error_analysis.py"
    click F "https://github.com/prakharrathi25/the-tool-bmwi/blob/main/pages/home_page.py"
</div>

<br> -->

When you open the tool, the first page you see is the **Home** page.

1. Your prediction journey starts on the **Data Prep** page. There, you upload the data, and do necessary preprocessing that would then feed into the model. [Click here](../data/7444_318010_BMWI_Enkelmann_Eckdaten_Zeitreihe_Kreise.xlsx) to download an Excel file containing data till May 2021. This Excel file contains the format of the input that our tool was tested on.
2. Once you "confirm" the preprocessed data on the **Data Prep** page, you can go to the **Model** page. The preprocessed data from the page before is automatically loaded. The predictions may take a while to run. The prediction results are cached, which means it should run faster the second time you try to predict the same data. 
3. The **Visualizations** page includes line plots and map visualizations to quickly understand the prediction results, e.g. which kreis has the highest unemployment rate, whether the trend for that kreis is going up or down.
4. The **Rankings** page contains kreis-level and grouped rankings of unemployment rates and their percentage changes. 
5. The **Error Analysis** page would be automatically loaded with the prediction results. This page helps you look closer into which kreise were harder to predict, and how that compares with their basic infrastructures, such as number of hospitals, number of schools etc.

<br>

<div class='mermaid'>
graph LR
    A1(First-time Users)
    A1-->A2[Step-By-Step Guide]
    A1-->A3[Tool]
    click A2 "../../steps/home/"
    click A3 "https://bmwi-tool.herokuapp.com/"
    style A2 fill:#CAEEFE,stroke:#2596be,color:#063970
    style A3 fill:#CAEEFE,stroke:#2596be,color:#063970
</div>

<br>

Now that you understand what you can expect, visit to the [**Step-By-Step Guide section**]('../steps/home/') of the documentation if necessary. We suggest that you open up the tool on a side-by-side window, so that you can follow and implement along with the guided instruction.

<br>

## Experienced Users

If you are an experienced user, you can dive right in the tool! 

<div class='mermaid'>
graph LR
    B1(Experienced Users)
    B1-->B2[Tool]
    B1-->B3[Error Handling]
    click B2 "https://bmwi-tool.herokuapp.com/"
    click B3 "../../steps/error/"
    style B2 fill:#CAEEFE,stroke:#2596be,color:#063970
    style B3 fill:#CAEEFE,stroke:#2596be,color:#063970
</div>

<br>

If you are encountering problems, it is likely that the problem and how to solve it is already noted in our documentation. You can visit the specific page in the **Step-By-Step Guide section**.

If you are encountering a problem that is not recorded in our documentation, please let us know. 

<br>

## Quick Access

Check out the Quick Access pages we built just for you!

<div class='mermaid'>
graph LR
    C1(Quick Access) 
    C1 --> C2[Prediction Results]
    C1 --> C3[Quick Access documentation]
    C1 --> C4[Quick Access tool page]
    click C2 "../../start/start/"
    click C3 "../../start/quick/"
    click C4 "../../start/quick/"
    style C2 fill:#CAEEFE,stroke:#2596be,color:#063970
    style C3 fill:#CAEEFE,stroke:#2596be,color:#063970
    style C4 fill:#CAEEFE,stroke:#2596be,color:#063970
</div>

<br>

<!-- - If you just want to get the prediction results for this quarter, [here]() is the link to download the excel file. -->
- If you want to quickly get a grasp of the project, the tool, and the documentation, [this page](../../start/start/) is for you.
- If you want to get a light interpreattion for the latest prediction results, the [home page](https://bmwi-tool.herokuapp.com/) of the tool provides rankings, and the [model page](https://bmwi-tool.herokuapp.com/) provides line plots and a map of Germany.

<br>

## Technical Users

The **Advanced Features section** contains detailed code walkthroughs.

<div class='mermaid'>
graph LR
    D1(Technical Users) 
    D1 --> D3[Technical Workflow page]
    D1 --> D4[Installation and Setup page]
    click D3 "../../advanced/tech_flow/"
    click D4 "../../advanced/installation/"
    style D3 fill:#CAEEFE,stroke:#2596be,color:#063970
    style D4 fill:#CAEEFE,stroke:#2596be,color:#063970
</div>

- The **[Technical Workflow page](../../advanced/tech_flow/)** explains the data model pipeline.
- Check out the **[Installation and Setup page](../../advanced/installation/)** to get started!

